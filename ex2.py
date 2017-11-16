'''
Created on Oct 1, 2017

@author: Apoll
'''
import math

def area_of_circle(r):
    area = (math.pi) * (r ** 2)
    area = round(area,3)
    print(area)
    return area

count = 0
n = 100
while n > 0:
    count = count + 1
    n = n // 10

print(count)