def findSnake():
    text_file = open('test.txt','r')
    lines = text_file.read().splitlines()
    for line in lines:
        if 'snake' in line:
            print(line)

if __name__ == '__main__':
    findSnake()