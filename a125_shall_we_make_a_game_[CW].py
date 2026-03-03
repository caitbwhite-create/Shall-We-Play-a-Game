import turtle
import random
import time

# --- Setup Screen ---
screen = turtle.Screen()
screen.setup(width=600, height=800)
screen.bgcolor("forestgreen")
screen.title("Crossy Road Python")
screen.tracer(0) 

# --- Register Shapes ---
try:
    screen.addshape("chicken.gif")
    screen.addshape("car1.gif")
    screen.addshape("train.gif")
    use_custom_icons = True
except:
    use_custom_icons = False
    print("GIF files not found. Using default shapes.")

# --- Drawing the Background ---
bg = turtle.Turtle()
bg.hideturtle()
bg.speed(0)

def draw_rect(color, x, y, w, h):
    bg.penup()
    bg.goto(x, y)
    bg.color(color)
    bg.begin_fill()
    for _ in range(2):
        bg.forward(w); bg.left(90)
        bg.forward(h); bg.left(90)
    bg.end_fill()

# Draw Grass and Roads
draw_rect("yellowgreen", -300, -400, 600, 800) 
road_positions = [-260, -20, 160] 

for y in road_positions:
    draw_rect("black", -300, y, 600, 100)
    bg.color("white")
    bg.pensize(3)
    for x in range(-280, 300, 60):
        bg.penup(); bg.goto(x, y + 45); bg.pendown(); bg.forward(20)

# --- Draw Train Tracks (Middle Position) ---
# This moves the track to the green space between the bottom and middle road
track_y_middle = -140  


# Draw the two long horizontal rails
draw_rect("saddlebrown", -300, track_y_middle + 10, 600, 7)
draw_rect("saddlebrown", -300, track_y_middle + 35, 600, 7)


# Draw the wooden ties (sleepers)
for x in range(-280, 300, 40):
    # This draws the vertical wood pieces across the rails
    draw_rect("saddlebrown", x, track_y_middle, 10, 50)

# --- The Player (Chicken) ---
player = turtle.Turtle()
player.penup()
if use_custom_icons:
    player.shape("chicken.gif")
else:
    player.shape("triangle")
    player.color("orange")
player.goto(0, -350)
player.setheading(90)

def move_up(): player.sety(player.ycor() + 40)
def move_down(): player.sety(player.ycor() - 40)
def move_left(): player.setx(player.xcor() - 40)
def move_right(): player.setx(player.xcor() + 40)

screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

#---End message---
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")

def show_message(message):
    pen.goto(0, 0)
    pen.write(message, align="center", font=("Courier", 36, "bold"))
    screen.update()
    time.sleep(1.5)
    pen.clear()

# --- Obstacles ---
cars = []
trains = []

def create_car(y_pos):
    new_car = turtle.Turtle()
    new_car.penup()
    if use_custom_icons:
        new_car.shape("car1.gif")
    else:
        new_car.shape("square")
        new_car.shapesize(stretch_wid=2, stretch_len=3)
        new_car.color("red")
    
    start_x = random.choice([-350, 350])
    new_car.goto(start_x, y_pos + 50)
    new_car.speed_val = random.randint(3, 6) if start_x == -350 else random.randint(-6, -3)
    cars.append(new_car)

def create_train(y_pos):
    new_train = turtle.Turtle()
    new_train.penup()
    if use_custom_icons:
        new_train.shape("train.gif")
    else:
        new_train.shape("square")
        new_train.shapesize(stretch_wid=2, stretch_len=8)
        new_train.color("gray")
    
    new_train.goto(-400, y_pos - 175)
    new_train.speed_val = 12 # Trains move fast
    trains.append(new_train)

# Spawn initial objects
for y in road_positions:
    for _ in range(2): 
        create_car(y)

create_train(70) # One train on the tracks

# --- Game Loop ---
while True:
    screen.update()
    time.sleep(0.02)
    
    # Move Cars
    for car in cars:
        car.setx(car.xcor() + car.speed_val)
        if car.xcor() > 350: car.goto(-350, car.ycor())
        if car.xcor() < -350: car.goto(350, car.ycor())
        if car.distance(player) < 30:
            show_message("Hit by a car!")
            player.goto(0, -350)



    # Move Trains
    for t in trains:
        t.setx(t.xcor() + t.speed_val)
        
        # Reset train if it goes off screen
        if t.xcor() > 600:
            t.goto(-800, t.ycor())

        # Improved Collision Detection for long objects:
        # Check if chicken is vertically close AND horizontally within the train's length
        x_dist = abs(t.xcor() - player.xcor())
        y_dist = abs(t.ycor() - player.ycor())
        
        # If using default shapes (stretch_len=8), the train is about 160 pixels wide
        if x_dist < 80 and y_dist < 30: 
            show_message("Smushed by a train!")
            player.goto(0, -350)

    # Win Condition
        if player.ycor() > 300:
            show_message("YOU SURVIVED!")
            player.goto(0, -350)
