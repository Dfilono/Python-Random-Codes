import turtle

def langton():
    window = turtle.Screen()
    window.bgcolor('white')
    window.screensize(1000, 1000)

    maps = {}

    ant = turtle.Turtle()
    ant.shape('square')
    ant.shapesize(0.5)
    ant.speed(10000)

    pos = coordinate(ant) 

    while True:
        step = 10

        if pos not in maps or maps[pos] == 'white':
            ant.fillcolor('black')
            ant.stamp()
            invert(maps, ant, 'black')
            ant.right(90)

            ant.forward(step)
            pos = coordinate(ant)

        elif maps[pos] == 'black':
            ant.fillcolor('white')
            invert(maps, ant, 'white')

            ant.stamp()
            ant.left(90)
            ant.forward(step)

            pos = coordinate(ant)

def coordinate(ant):
    return (round(ant.xcor()), round(ant.ycor()))

def invert(grid, ant, color):
    grid[coordinate(ant)] = color

langton()