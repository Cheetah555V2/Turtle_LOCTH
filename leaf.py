pen_color = "green"
pen_size = 1
turtle_shape = "turtle"

import turtle

def draw_stem(max_iteration=3, curr_angle = 90, curr_iteration = 0, curr_pen_size = 1, curr_turtle_size = 1, curr_leaf_size=400 ,size_factor = 0.2, facing = 1, prev_position = (0,0), leaf_number = 2):
    bob = turtle.Turtle()
    bob.speed(0)
    bob.settiltangle(curr_angle)
    bob.pencolor(pen_color)
    bob.pensize(curr_pen_size)
    bob.shape(turtle_shape)
    bob.penup()
    bob.left(90)
    bob.goto(prev_position)
    bob.pendown()
    bob.turtlesize(curr_turtle_size*size_factor)

    if curr_iteration < max_iteration:
        for i in range(leaf_number):
            bob.circle(curr_leaf_size, extent = 30/leaf_number)
            draw_stem(curr_angle = 90 + facing*90, curr_iteration = curr_pen_size + 1, curr_leaf_size=curr_leaf_size*size_factor, prev_position = bob.position())
    
    else:
        pass
    
    

window = turtle.Screen()
window.screensize(600,600)

draw_stem(prev_position=(0,-100))

turtle.done()