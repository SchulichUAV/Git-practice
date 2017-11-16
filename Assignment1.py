import pygame
import sys
import math
import random


class Car():
    numberOfCars = 0

    def __init__(self, x, y, isHorizontal, length):
        Car.numberOfCars += 1
        self.id = Car.numberOfCars
        self.x, self.y = x, y
        self.isHorizontal = isHorizontal
        if(isHorizontal):
            self.rect = pygame.rect.Rect(x * 64, y * 64, length * 64, 64)
        else:
            self.rect = pygame.rect.Rect(x * 64, y * 64, 64, length * 64)
        self.length = length
        self.isEasing = False
        self.occupied = []
        self.update()
        self.color = self.generateColor(60)

    @staticmethod
    def generateColor(x):
        ''' Generate a nice pastel colour '''
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        r_ = ((100 - x) * r + x * 255) / 100
        g_ = ((100 - x) * g + x * 255) / 100
        b_ = ((100 - x) * b + x * 255) / 100

        print(r_, g_, b_)
        return (r_, g_, b_)

    def update(self):
        self.occupied = []
        if self.isHorizontal:
            for x in range(0, self.length):
                self.occupied.append([self.x + x, self.y])
        else:
            for y in range(0, self.length):
                self.occupied.append([self.x, self.y + y])
        self.ease()

    def ease(self):
        if self.isEasing:
            self.rect.x = self.rect.x * 0.90 + self.x * 64 * 0.10
            self.rect.y = self.rect.y * 0.90 + self.y * 64 * 0.10
            if self.isHorizontal and math.fabs(self.rect.x - (self.x * 64)) < 10:
                self.rect.x = self.x * 64
                self.isEasing = False
            elif not self.isHorizontal and math.fabs(self.rect.y - (self.y * 64)) < 10:
                self.rect.y = self.y * 64
                self.isEasing = False

    def __del__(self):
        Car.numberOfCars -= 1


class RushHour():

    def __init__(self, row, col, end):
        self.table = self.generateTable(row, col)
        self.end = end
        self.printTable()
        self.listOfCars = []

    def generateTable(self, row, col):
        table = [[99 for x in range(col)] for y in range(row)]

        for x in range(row):
            for y in range(col):
                table[x][y] = '.'
        return table

    def addCar(self, x, y, isHorizontal, length):
        if not self.isLegalMove(x, y, isHorizontal, length):
            return
        car = Car(x, y, isHorizontal, length)
        self.listOfCars.append(car)
        self.updateTable()

    def isLegalMove(self, x, y, isHorizontal, length, id='.'):
        if x < 0 or y < 0:
            print("OUT OF BOUNDS NEG")
            return False

        try:
            if str(self.table[y][x]) == '.' or self.table[y][x] == id or self.table[y][x] == '@':
                if isHorizontal:
                    for i in range(length):
                        if str(self.table[y][x + i]) != '.' and self.table[y][x + i] != id and self.table[y][x + i] != '@':
                            print('(2) OBSTUCTION AT: ', x, i)
                            return False
                else:
                    for j in range(length):
                        if str(self.table[y + j][x]) != '.' and self.table[y + j][x] != id and self.table[y + j][x] != '@':
                            print('(3) OBSTUCTION AT: ', j, x)
                            return False
            else:
                print("(1) OBSTRUCTION AT: ", x, y)
                return False
        except Exception as e:
            print("OUT OF BOURNDS", e)
            return False
        return True

    def updateTable(self):
        self.table = self.generateTable(len(self.table), len(self.table[0]))
        self.table[self.end[1]][self.end[0]] = '@'
        for car in self.listOfCars:
            self.table[car.y][car.x] = car.id
            if car.isHorizontal:
                for index in range(car.length):
                    self.table[car.y][car.x + index] = car.id
            else:
                for index in range(car.length):
                    self.table[car.y + index][car.x] = car.id

    def isVictory(self):
        car = self.getCar(1)
        if car.isHorizontal:
            for index in range(0, car.length):
                if car.x + index == self.end[0] and car.y == self.end[1]:
                    return True
        else:
            for index in range(0, car.length):
                if car.x == self.end[0] and car.y + index == self.end[1]:
                    return True
        return False

    def printListOfCars(self):
        for car in self.listOfCars:
            print(car.id)

    def moveCar(self, id, move):
        car = self.getCar(id)
        valid = False

        if move > 0:
            move = 1
        elif move < 0:
            move = -1

        if car is not None:
            if car.isHorizontal:
                valid = self.isLegalMove(
                    car.x + (1 * move), car.y, True, car.length, id=id)
                if valid:
                    car.x += 1 * move
            else:
                valid = self.isLegalMove(
                    car.x, car.y + (1 * move), False, car.length, id=id)
                if valid:
                    car.y += 1 * move
            car.update()
        else:
            print("that car doesn't exist")
        self.clearTableOfCar(id)
        self.updateTable()

    def userMove(self):
        return int(input('+n/-n: '))

    def clearTableOfCar(self, id):
        for y in range(len(self.table)):
            for x in range(len(self.table[y])):
                if self.table[y][x] == id:
                    self.table[y][x] = '.'

    def getCar(self, id):
        for car in self.listOfCars:
            if car.id == id:
                return car

    def printTable(self):
        print()
        for index in range(len(self.table[1])):
            print("   {:^1}".format(str(index)), end='')
        print(end='\n')
        for index, row in enumerate(self.table):
            print(index, end=' ')
            for col in row:
                print("{:^4}".format(str(col)), end='')
            print(end='\n')

    def getTable(self):
        return self.table


class GUI():
    def __init__(self, table, game):
        self.game = game
        pygame.init()
        self.table = table
        size = width, height = 640, 640
        self.backgroundColor = Car.generateColor(50)
        self.screen = pygame.display.set_mode(size)
        self.focusedCar = None

    def render(self):
        import time
        fps = 59.99
        time_delta = 1 / fps
        while True:
            time.sleep(time_delta)
            self.listen()
            self.screen.fill(self.backgroundColor)
            color = (0, 255, 0)
            focusedColor = (0, 0, 255)
            border = 0
            for x in range(len(self.table)):
                for y in range(len(self.table[0])):
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * 64, y * 64, 64, 64), 1)

            for car in self.game.listOfCars:
                car.update()
                if self.focusedCar == car:
                    pygame.draw.rect(self.screen, car.color, car.rect)
                    pygame.draw.rect(self.screen, focusedColor, car.rect, 5)
                else:
                    pygame.draw.rect(self.screen, car.color, car.rect, border)
                color = (0, 255, 0)

            color = (255, 255, 0)
            pygame.draw.rect(
                self.screen, color, (self.game.end[0] * 64, self.game.end[1] * 64, 64, 64), border)
            pygame.display.update()

    def listen(self):
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for car in self.game.listOfCars:
                    if(car.rect.collidepoint(x, y)):
                        self.focusedCar = car
                        self.isEasing = False
                        if self.focusedCar.isHorizontal:
                            self.offset = car.rect.x - x
                        else:
                            self.offset = car.rect.y - y

            elif event.type == pygame.MOUSEMOTION and self.focusedCar is not None:
                if self.focusedCar.isHorizontal:
                    self.game.moveCar(self.focusedCar.id, int(
                        round((x + self.offset) / 64, 0)) - (self.focusedCar.x))
                    if(self.focusedCar.x == round((x + self.offset) / 64, 0)):
                        if(self.game.isLegalMove(math.ceil((x + self.offset) / 64), int(self.focusedCar.y), True, self.focusedCar.length, self.focusedCar.id)):
                            if(self.game.isLegalMove((x + self.offset) // 64, int(self.focusedCar.y), True, self.focusedCar.length, self.focusedCar.id)):
                                self.focusedCar.rect.x = x + self.offset
                else:
                    self.game.moveCar(self.focusedCar.id, int(
                        round((y + self.offset) / 64, 0)) - (self.focusedCar.y))
                    if(self.focusedCar.y == round((y + self.offset) / 64, 0)):
                        if(self.game.isLegalMove(int(self.focusedCar.x), math.ceil((y + self.offset) / 64), False, self.focusedCar.length, self.focusedCar.id)):
                            if(self.game.isLegalMove(int(self.focusedCar.x), (y + self.offset) // 64, False, self.focusedCar.length, self.focusedCar.id)):
                                self.focusedCar.rect.y = y + self.offset
                self.game.updateTable()
                self.game.printTable()

            elif event.type == pygame.MOUSEBUTTONUP and self.focusedCar is not None:
                self.focusedCar.isEasing = True
                self.game.updateTable()
                self.focusedCar = None
            else:
                pass

    def piyel2Table(self, x, y):
        return (x // 64, y // 64)

    def update(self, table):
        self.table = table


if __name__ == '__main__':
    game = RushHour(10, 10, (9, 5))
    print(game.addCar(0, 5, True, 3))
    print(game.addCar(3, 0, True, 3))
    print(game.addCar(5, 5, False, 5))
    game.printTable()
    gui = GUI(game.table, game)

    while(not game.isVictory()):
        gui.render()
        user = int(input('select car: '))
        game.moveCar(user, game.userMove)
        game.printTable()
        gui.update(game.table)
        print('Victory State: ', game.isVictory())
