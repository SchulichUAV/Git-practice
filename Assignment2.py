'''
Created on Oct 13, 2017

@author: Bryan Huynh
'''
import turtle
import random

windowWidth, windowHeight = 500, 500


def init():
    '''
    will initalize all the game settings
    sets the turtles and their colors
    also starts game
'''
    alex = turtle.Turtle()
    alice = turtle.Turtle()
    wn = turtle.Screen()
    alex.shape("turtle")
    alex.color('blue')
    alice.shape("turtle")
    alice.color('red')
    wn.setup(windowWidth, windowHeight)
    loop(alex, alice, windowWidth, windowHeight)
    wn.mainloop()


def loop(alex, alice, width, height):
    '''
    runs the actual game
    it will count and display the amount of iterations that have occurred
'''
    step = 0
    alice.penup()
    # move alice to a random location inside the window
    spawnTurtleRandom(alice, width, height)
    alice.pendown()
    while(True):
        # checks if the turtles are still in the bounds of the window
        if not (turtleInbound(alice, width, height)):
            # relocates them within the window if they're out of bounds
            spawnTurtleRandom(alice, width, height)
        if not (turtleInbound(alex, width, height)):
            spawnTurtleRandom(alex, width, height)

        # distance between alice and alex is calculated
        distance = getDistance(alex, alice)
        # steps and distance is drawn
        drawInfo(step, distance, width, height)

        # checks if the game is over. aka distance between alice and alex is less than 30
        if gameOver(distance):
            # break out of the while loop that runs the game
            break

        # initiates the turtle alex to move based on user input
        moveInput(alex, "Alex")
        # tells alice to move randomly
        moveRand(alice)
        step += 1                                               # increase the turn counter


def gameOver(distance):
    '''
    checks if the games over. ie is that distance less or equal to 30
'''
    if(distance <= 30):
        return True
    return False


def getDistance(t1, t2):
    '''
    calculates the distance between two turtles
    I made my own method because calculate the distance between two turtles instead of a turtle and a point is easier
'''
    distance = round(t1.distance(t2.xcor(), t2.ycor()), 2)
    return distance


def drawInfo(step, distance, width, height):
    '''
    will write on the window the amount of steps the game has taken
    the text will be postioned on the top centre of the window
    and the distance between turtles.
'''
    turtle.penup()
    turtle.hideturtle()
    turtle.setpos((width) / -4, (height) / 2 - 16)
    turtle.clear()
    turtle.write("Step# " + str(step) + ". Distance between Alex & Alice: " +
                 str(distance), False, align="left")


def moveInput(turtle, name):
    '''
    gets an input from the user and will move the turtle forward or backwards with (W|S) respectively or rotates left or right with (A|D) respectively
        having a string name is required to keep the code more modular for different turtles.
'''
    while(True):
        # asks for user input. Converts it to lower case, just in case the user forgot to turn off CAPSLOCK, as people occassionally do
        user = input("Move " + name + ": ").lower()
        if(user == 'w'):                                                        # moves toward 30
            move(turtle, 0, 30)
        # turns to the right 45 degrees
        elif(user == 'd'):
            move(turtle, -45, 0)
        # turns to the left 45 degrees
        elif(user == 'a'):
            move(turtle, 45, 0)
        # flees like a coward for 30
        elif(user == 's'):
            move(turtle, 0, -30)
        else:
            # prints that the user didn't input a valid command
            print("'" + user + "' is not recognized as a movement. Retype")
            # forces the while loop to start over
            continue
        # if the user input managed to get pass the invalid input, the loop will break
        break


def turtleInbound(turtle, width, height):
    '''
checks if the turtle is still in the window
returns false if outside
returns true if inside
'''
    x = turtle.xcor()
    y = turtle.ycor()

    # checks if the turtle is outside the x range
    if(x > width / 2) or (x < width / -2):
        return False
    # checks if the turtle is outside the y range
    if(y > height / 2) or(y < height / -2):
        return False
    return True


def spawnTurtleRandom(turtle, width, height):
    '''
    relocates the turtle within the bounds of the window
'''

    x = random.randint(width // -2, width // 2)
    y = random.randint(height // -2, height // 2)
    turtle.setpos(x, y)


def moveRand(turtle):
    '''
    automates the turtle to move
    will move forward (2/3)'s of the time
    will move left or right (1/3) of the time
'''
    rand = random.randint(
        0, 5)                                 # generates a number from [1,5]
    if(rand <= 3):
        # if the number is less than 4, then move forward 20
        move(turtle, 0, 20)
    elif(rand == 4):
        # if the number is equal to 4, then turn 90 left
        move(turtle, 90, 0)
    elif(rand == 5):
        # if the number is equal to 5, then turn 90 right
        move(turtle, -90, 0)


def move(turtle, degree, distance):
    '''
    will turn or move the turtle
    I had this method do both turning and moving because it made it easier to input 0 if you don't want the turtle to do a certain action

'''
    heading = turtle.heading()
    # adds the degree of change to the current state
    turtle.setheading(heading + degree)
    # moves the turtle forward by a input distance
    turtle.forward(distance)


if __name__ == "__main__":

    init()
