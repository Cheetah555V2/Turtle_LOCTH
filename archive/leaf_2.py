# barnsley_fern_fast.py
import turtle

# ======== User Parameters ========
dot_size = 3          # Size of each dot
depth = 8             # Depth of recursion (7 = 16,384 points, 8 = 65,536)
dot_color = "green"   # Dot color (e.g., "green", "lime", "#00AA00")
background = "white"  # Background color
# =================================

# Barnsley affine transforms (exact IFS)
def f1(x, y): return 0.0, 0.16 * y
def f2(x, y): return 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
def f3(x, y): return 0.20 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
def f4(x, y): return -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44

TRANSFORMS = (f1, f2, f3, f4)

def draw_ifs_recursive(pen, x, y, depth, dot_size):
    """Recursively apply Barnsley transforms and draw at base depth."""
    if depth == 0:
        pen.goto(x, y)
        pen.dot(dot_size)
        return

    next_depth = depth - 1
    for f in TRANSFORMS:
        nx, ny = f(x, y)
        draw_ifs_recursive(pen, nx, ny, next_depth, dot_size)

def main():
    # Setup screen
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.setworldcoordinates(-3.0, -0.5, 3.0, 10.5)
    screen.bgcolor(background)

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    pen.color(dot_color)

    # Disable auto-updating for massive speed boost
    screen.tracer(0, 0)

    # Draw centered fern starting at origin
    draw_ifs_recursive(pen, 0.0, 0.0, depth, dot_size)

    # Final screen update
    screen.update()
    screen.title(f"Barnsley Fern — depth={depth}, color={dot_color}")

    screen.exitonclick()

if __name__ == "__main__":
    main()
