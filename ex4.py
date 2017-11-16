#import sys
#sys.setrecursionlimit(15000)

def print_triangular_numbers(n):
    def recursion(n):
        if n <= 1:
            return 0
        return n + recursion(n - 1)
    for i in range(1,n+1):
        print(i,"     ", recursion(i) + 1 )
'''
def num_digits(n):
    n = (n**2)**(1/2)
    count = 1
    while n >= 9:
        count = count + 1
        n = n // 10
    return count
'''
def num_digits(n):
    n = (n**2)**(1/2)
    if(n <= 9):
        return 1
    return 1 + num_digits(n // 10)
