# Import the Turtle Graphics Module and random module
import turtle
import random

# Define constants
WIDTH = 600  # Screen width
HEIGHT = 600  # Screen hight
DELAY = 100  # 400 millisecond playback delay
FOOD = 20  # Food size

input_go = True #Prevent double input. Double inoput may cause snake to collide with itself when it shouldn't

def game_loop():
    stamper.clearstamps()  # Clears existing snake

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collision
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
            or new_head[1] < - HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        reset_game()
    else:
        # Moves snake by adding head and removing tail
        snake.append(new_head)
        global input_go
        input_go = True

        #Check if head meets nip
        if not nip_collision():
            snake.pop(0)

        # Draw initial Snake
        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        #Score bar
        screen.title(f"Snake Game       Omnoms nommed: {score}")
        # Refresh Screen with new snake
        screen.update()

        # Moves snake by refreshing screen on the defined interval
        turtle.ontimer(game_loop, DELAY)


def nip_collision():
    global nip_pos, score
    if get_distance(snake[-1], nip_pos) < 20:
        nip_pos = get_snakenip_pos()
        nip.goto(nip_pos)
        score += 1
        return True
    return False


def get_snakenip_pos():
    x = random.randint(- WIDTH / 2 + FOOD, WIDTH / 2 - FOOD)
    y = random.randint(- HEIGHT / 2 + FOOD, HEIGHT / 2 - FOOD)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # pytagoras
    return distance

#Auto reset on death
def reset_game():
    global score, snake, snake_direction, nip_pos
    # Snake starting coordinates
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    snake_direction = "Up"
    score = 0
    nip_pos = get_snakenip_pos()
    nip.goto(nip_pos)
    game_loop()


# Movement control
offsets = {
    "Up": (0, 20),
    "Down": (0, -20),
    "Left": (-20, 0),
    "Right": (20, 0)
}

def bind_dirKeys():
    screen.onkeypress(lambda: set_snake_direction("Up"), "Up")
    screen.onkeypress(lambda: set_snake_direction("Down"), "Down")
    screen.onkeypress(lambda: set_snake_direction("Right"), "Right")
    screen.onkeypress(lambda: set_snake_direction("Left"), "Left")
    screen.onkeypress(lambda: exit("Escape"), "Escape")

def set_snake_direction(direction):
    global snake_direction, input_go
    if input_go:
        if direction == "Up":
            if snake_direction != "Down": #Can't back up into self
                snake_direction = "Up"
        elif direction == "Down":
            if snake_direction != "Up": #Can't back up into self
                snake_direction = "Down"
        elif direction == "Left":
            if snake_direction != "Right": #Can't back up into self
                snake_direction = "Left"
        elif direction == "Right":
            if snake_direction != "Left": #Can't back up into self
                snake_direction = "Right"
        input_go = False



# Graphics window
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Exercise")
screen.bgcolor("dark grey")
screen.tracer(0)  # Turns off default animation

# Create stamp for graphics
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.color("Cyan")
stamper.penup()

# Event handlers
screen.listen()
bind_dirKeys()

#Food
nip = turtle.Turtle()
nip.shape("circle")
nip.color("Dark Cyan")
nip.shapesize(FOOD / 20)
nip.penup()

reset_game()

# Terminate nicely
turtle.done()
