import sqlite3
import datetime
import sys
import traceback
import atexit
import os
curfilePath = os.path.abspath(__file__)
curDir = os.path.abspath(os.path.join(curfilePath, os.pardir))
global PARENT_DIRECTORY
PARENT_DIRECTORY = os.path.abspath(os.path.join(curDir, os.pardir))
global FILE_PATH
FILE_PATH = PARENT_DIRECTORY


def changeFilePath(path):
    global FILE_PATH
    global PARENT_DIRECTORY
    print(FILE_PATH)
    FILE_PATH = PARENT_DIRECTORY + '\\' + path


def printLog(data, message=None, e=None, isInput=False):
    conn = sqlite3.connect(FILE_PATH + "\log.db")
    dataType = type(data)
    atexit.register(endLog)

    data = str(data)
    now = datetime.datetime.now()

    c = conn.cursor()

    stack = traceback.extract_stack()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime('%H:%M:%S:%f')[:]

    filePath = str(stack[len(stack) - 2][0])
    filePath = filePath[::-1]
    filePath = filePath[:filePath.find('\\')]
    if len(filePath) == str(stack[len(stack) - 2][0]):
        filePath = filePath[:filePath.find('/')]
    filePath = filePath[::-1]

    print(filePath)

    line = int(stack[len(stack) - 2][1])
    time = str(time)

    if e is not None:
        std = 'error'
        data = e
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line = exc_tb.tb_lineno
        dataType = 'error'
    elif isInput:
        std = 'input'
    else:
        std = 'output'

    data = str(data)
    dataType = str(dataType)
    message = str(message)

    try:
        c.execute(
            'CREATE TABLE log (std TEXT, date TEXT, time TEXT, file TEXT, line INT, message TEXT, data TEXT, type TEXT)')
    except:
        pass

    c.execute('INSERT INTO log VALUES(?,?,?,?,?,?,?,?)',
              (std, date, time, filePath, line, message, data, dataType))
    print('{st:<10} {d:<10} {ti:<9} {f:<20} {ln:<10} {ms:<15} {da:<30} {ty:<50}'.format(
        st=std, d=date, ti=time, f='File: ' + filePath, ln='Line: ' + str(line), ms='message: ' + message, da='data: ' + data, ty=dataType))
    conn.commit()


def endLog():
    try:
        conn = sqlite3.connect(FILE_PATH + "\log.db")
    except:
        print('could not find database')
    c = conn.cursor()
    c.execute('select * from log')
    db = c.fetchall()
    row = db[-1]
    print(row)
    if row[0] == "terminated":
        return

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime('%H:%M:%S:%f')
    ms = 'terminated'
    c.execute('INSERT INTO log VALUES(?,?,?,?,?,?,?,?)',
              (ms, date, time, 0, 0, 0, 0, 0))
    conn.commit()
    conn.close()


def readLog():
    try:
        conn = sqlite3.connect(FILE_PATH + "\log.db")
    except:
        print('could not find database')

    c = conn.cursor()
    c.execute('select * from log')
    db = c.fetchall()
    print(db)
    for row in db:
        printRow(row)


def printLastLog():
    try:
        conn = sqlite3.connect(FILE_PATH + "\log.db")
    except:
        print('could not find database')

    c = conn.cursor()
    c.execute('select * from log')
    db = c.fetchall()
    list = []
    for row in db[-2::-1]:
        if row[0] == 'terminated':
            break
        list.append(row)

    list = list[::-1]
    for row in list:
        printRow(row)


def printRow(row):
    std = row[0]
    date = row[1]
    time = row[2]
    filePath = row[3]
    line = row[4]
    message = row[5]
    data = row[6]
    dataType = row[7]
    print('{st:<10} {d:<10} {ti:<9} {f:<20} {ln:<10} {ms:<15} {da:<30} {ty:<50}'.format(
        st=std, d=date, ti=time, f='File: ' + filePath, ln='Line: ' + str(line), ms='message: ' + message,
        da='data: ' + data, ty=dataType))


def read():
    user = int(input('(1) print entire log \n'
                     '(2) print most recent \n'))
    if(user == 1):
        readLog()
    elif(user == 2):
        printLastLog()


if __name__ == '__main__':
    read()
