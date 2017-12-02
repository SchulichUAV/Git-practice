# TODO
# 1. Check atexit on errors and make sure that it runs on Ctrl+C
# 2. Optimize the read last entry with SQL commands (Look up where, if, order by commands. Use W3Schools as a resource.)
# 3. Fix file paths so. Adding default param for print_log and make sure PrintLog.py and ex5.py read the same db.
# 4. Keep up the good work!

import sqlite3
import datetime
import sys
import traceback
import atexit
import os

cur_file_path = os.path.abspath(__file__)
cur_dir = os.path.abspath(os.path.join(cur_file_path, os.pardir))

PARENT_DIRECTORY = os.path.abspath(os.path.join(cur_dir, os.pardir))
global FILE_PATH
FILE_PATH = PARENT_DIRECTORY
print(FILE_PATH)

def change_file_path(path):
    global FILE_PATH
    print(FILE_PATH)
    FILE_PATH = os.path.join(PARENT_DIRECTORY, path)


def __parse_path_from_stack(stack):
    file_path = str(stack[len(stack) - 2][0])
    return os.path.basename(file_path)


def __parse_line_from_stack(stack):
    return int(stack[len(stack) - 2][1])


def print_log(data, message=None, e=None, isInput=False):
    conn = sqlite3.connect(os.path.join(FILE_PATH, "log.db"))
    data_type = type(data)
    atexit.register(end_log) # Todo Test atexit or look it up

    now = datetime.datetime.now()

    c = conn.cursor()

    stack = traceback.extract_stack()
    file_path = __parse_path_from_stack(stack)

    date_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")

    line = __parse_line_from_stack(stack)

    if e is not None:
        std = 'error'
        data = e
        exc_type, exc_obj, exc_tb = sys.exc_info()
        line = exc_tb.tb_lineno
        data_type = 'error'
    elif isInput:
        std = 'input'
    else:
        std = 'output'

    data = str(data)
    data_type = str(data_type)
    message = str(message)

    c.execute(
        'CREATE TABLE IF NOT EXISTS log (std TEXT, date_time TIME, file TEXT, line INT, message TEXT, data TEXT, type TEXT)'
    )

    c.execute('INSERT INTO log VALUES (?,?,?,?,?,?,?)',
              (std, date_time, file_path, line, message, data, data_type)
    )

    print(
        '{st:<10} {d:<} {f:<30} {ln:<10} {ms:<15} {da:<30} {ty:<50}'.format(
            st=std,
            d=date_time,
            f='File: ' + file_path,
            ln='Line: ' + str(line),
            ms='message: ' + message,
            da='data: ' + data,
            ty=data_type)
    )

    conn.commit()
    conn.close()


def end_log():
    DATABASE_PATH = os.path.join(FILE_PATH, "log.db")
    try:
        conn = sqlite3.connect(DATABASE_PATH)
    except:
        print('Could not find database {}'.format(DATABASE_PATH))
        return None
    c = conn.cursor()
    c.execute('SELECT std FROM log ORDER BY date_time DESC LIMIT 1')
    db = c.fetchone()
    should_run_terminate = False
    if not db:
        # DB is empty
        should_run_terminate = True
    else:
        last_std = db[0]
        if last_std != "terminated":
            should_run_terminate = True

    if should_run_terminate:
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S:%f")
        ms = 'terminated'
        c.execute('INSERT INTO log VALUES (?,?,?,?,?,?,?)',
                  (ms, date_time, 0, 0, 0, 0, 0))
    conn.commit()
    conn.close()


def read_log():
    conn = sqlite3.connect(os.path.join(FILE_PATH, "log.db"))
    c = conn.cursor()
    c.execute('select * from log')
    db = c.fetchall()
    print(db)
    for row in db:
        print_row(row)

    conn.close()


def print_last_log():
    conn = sqlite3.connect(FILE_PATH + "\log.db")

    c = conn.cursor()
    # TODO SQLite Optimize
    c.execute('select * from log')
    db = c.fetchall()
    list = []
    for row in db[-2::-1]:
        if row[0] == 'terminated':
            break
        list.append(row)

    list = list[::-1]
    for row in list:
        print_row(row)

    conn.close()


def print_row(row):
    std = row[0]
    date_time = row[1]
    filePath = row[2]
    line = row[3]
    message = row[4]
    data = row[5]
    dataType = row[6]
    print('{st:<10} {d:<30} {f:<20} {ln:<10} {ms:<15} {da:<30} {ty:<50}'.format(
        st=std, d=date_time, f='File: ' + filePath, ln='Line: ' + str(line), ms='message: ' + message,
        da='data: ' + data, ty=dataType))


def read():
    while True:
        user = int(input('(1) print entire log \n'
                         '(2) print most recent \n'
                         '(3) exit \n'))
        if user == 1:
            read_log()
        elif user == 2:
            print_last_log()
        elif user == 3:
            exit(0)
        else:
            print("You did not enter 1, 2 or 3.")

if __name__ == '__main__':
    read()
