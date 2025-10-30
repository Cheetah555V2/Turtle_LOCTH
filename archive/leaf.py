import turtle
import random

maximum_iterations = 100
dot_size = 2
dot_color = "green"

alex = turtle.Turtle()
alex.penup()
alex.speed(0)
x = 0.0
y = 0.0
t = 0
xn = 0.0
yn = 0.0
while t < maximum_iterations:
    r = random.random()
    if r < 0.01:
        xn = 0.0
        yn = (0.16 * y)*100
    elif r < 0.86:
        xn = (0.85*x + 0.04*y)*100
        yn = (-0.04*x + 0.85*y + 1.6)*100
    elif r < 0.93:
        xn = (0.2*x - 0.26*y)*100
        yn = (0.23*x + 0.22*y + 1.6)*100
    else:
        xn = (-0.15*x + 0.28*y)*100
        yn = (0.26*x + 0.24*y + 0.44)*100
    
    alex.goto((xn,yn))
    alex.dot(dot_size, dot_color)

