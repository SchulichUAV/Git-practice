def foo(n):
    n = n%2
    print(n)
    n = n%3
    print(n)
    n = n%5
    print(n)
    if(n == 0):
        return True
    else: 
        return False
    
print(foo(int(input())))