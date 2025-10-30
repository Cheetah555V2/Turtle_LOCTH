import turtle
import threading
import queue
import os
import time
import random

# ===== USER PARAMETERS =====
dot_size = 2                    # ขนาดของจุด
depth = 50000                   # จำนวนจุด (iterations / points)
speed = 0                       # ความเร็วของเต่า (0 = เร็วที่สุด, 1-10 = ช้า-->เร็ว)
hide_turtle = False              # ซ่อนตัวเต่าหรือไม่
dot_color = "green"               # สีของจุด
background = "white"            # สีพื้นหลัง










# Barnsley transforms & probabilities (classic)

render_while_drawing = False
def f1(x, y): return 0.0, 0.16 * y
def f2(x, y): return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
def f3(x, y): return 0.20 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
def f4(x, y): return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

TRANSFORMS = (f1, f2, f3, f4)
PROBS = (0.01, 0.85, 0.07, 0.07)

# cumulative probabilities for fast selection
cummulative_probs = []
acc = 0.0
for p in PROBS:
    acc += p
    cummulative_probs.append(acc)

def pick_transform_index(r):
    # r in [0,1); linear scan of 4 values is fine and fast
    for i, cp in enumerate(cummulative_probs):
        if r < cp:
            return i
    return len(cummulative_probs) - 1

# Producer/consumer queues
draw_queue = queue.Queue(maxsize=256)  # holds chunks (lists) of (x,y) points
CHUNK_SIZE = 2000                       # number of points per chunk (tweak for perf)

def worker_generate_points(iterations, seed, skip_initial=20):
    """
    Generate `iterations` points using the random iteration method.
    Push chunks to draw_queue. At the end push a "__WORKER_DONE__" sentinel.
    """
    rnd = random.Random(seed)
    x = 0.0
    y = 0.0
    buf = []

    # Burn-in to reach attractor
    for _ in range(skip_initial):
        idx = pick_transform_index(rnd.random())
        x, y = TRANSFORMS[idx](x, y)

    for i in range(iterations):
        idx = pick_transform_index(rnd.random())
        x, y = TRANSFORMS[idx](x, y)
        buf.append((x, y))

        if len(buf) >= CHUNK_SIZE:
            draw_queue.put(buf)
            buf = []

    if buf:
        draw_queue.put(buf)
    # signal done
    draw_queue.put("__WORKER_DONE__")

def consume_and_draw(num_workers, screen, pen, batch_update_every=1, render_after=False):
    """
    Main-thread consumer that draws chunks from draw_queue.
    - batch_update_every: how many chunks to draw before calling screen.update() when rendering while drawing.
    - render_after: if True, don't call screen.update() until everything is drawn.
    """
    finished = 0
    chunks_since_update = 0

    while True:
        item = draw_queue.get()
        if item == "__WORKER_DONE__":
            finished += 1
            draw_queue.task_done()
            if finished >= num_workers:
                break
            continue

        pts = item
        pen.penup()
        for (x, y) in pts:
            pen.goto(x, y)
            pen.dot(dot_size)

        # If we should render while drawing (render_after == False), update periodically:
        if not render_after:
            chunks_since_update += 1
            if chunks_since_update >= batch_update_every:
                screen.update()
                chunks_since_update = 0

        draw_queue.task_done()

    # If rendering after drawing, do one final update now
    if render_after:
        screen.update()

def main():
    # determine workers
    num_cpus = os.cpu_count() or 4
    num_workers = min(max(1, num_cpus), 8)

    # split iterations among workers
    base = depth // num_workers
    remainder = depth % num_workers
    iterations_per_worker = [base + (1 if i < remainder else 0) for i in range(num_workers)]

    # turtle setup (main thread)
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.setworldcoordinates(-3.0, -0.5, 3.0, 10.5)
    screen.bgcolor(background)

    pen = turtle.Turtle()
    if hide_turtle:
        pen.hideturtle()
    pen.speed(speed)
    pen.penup()
    pen.color(dot_color)

    # We always use manual updates (tracer(0,0)) for best throughput.
    # When render_while_drawing == True we will only call screen.update() once at the end.
    # When False we will call update periodically inside consume_and_draw.
    screen.tracer(0, 0)

    # Start worker threads (they only generate points)
    workers = []
    for i, iters in enumerate(iterations_per_worker):
        seed = int(time.time() * 1000) ^ (i * 99991)
        t = threading.Thread(target=worker_generate_points, args=(iters, seed))
        t.daemon = True
        t.start()
        workers.append(t)

    # Draw in main thread (blocks until done)
    try:
        # Choose how often to call screen.update() when rendering while drawing.
        # If you want fewer updates (faster) increase this number.
        batch_update_every = 1  # update after every chunk
        consume_and_draw(num_workers, screen, pen,
                         batch_update_every=batch_update_every,
                         render_after=render_while_drawing)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # final title & click-to-close
        screen.title(f"Barnsley Fern (chaos-game, points={depth})")
        screen.exitonclick()

if __name__ == "__main__":
    t0 = time.time()
    mode = "render-after" if render_while_drawing else "render-during"
    print(f"Chaos-game Barnsley: points={depth}, dot_size={dot_size}, color={dot_color}, mode={mode}")
    main()
    print("Done in %.2f s" % (time.time() - t0))
