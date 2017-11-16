import sqlite3
import datetime
import sys
import traceback
import atexit

def printLog(data, message= None, e=None, isInput = False):
	conn = sqlite3.connect("log.db")
	data_type = type(data)
	atexit.register(endLog)

	data = str(data)
	now = datetime.datetime.now()

	c = conn.cursor()

	stack = traceback.extract_stack()

	date = now.strftime("%Y-%m-%d")
	time = now.strftime('%H:%M:%S')

	filePath = str(stack[len(stack) - 2][0])

	filePath = filePath[::-1]
	filePath = filePath[:filePath.find('/')]
	filePath = filePath[::-1]

	line = int(stack[len(stack) - 2][1])
	time = str(time)

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
	try:
		c.execute('CREATE TABLE log (STD TEXT, DATE TEXT, TIME TEXT, FILE TEXT, LINE INT, MESSAGE TEXT, DATA TEXT, TYPE TEXT)')
	except:
		pass

	c.execute('INSERT INTO log VALUES(?,?,?,?,?,?,?,?)', (std , date, time, filePath, line, message, data, data_type))
	print('{st:<10} {d:<10} {ti:<9} {f:<20} {ln:<10} {ty:<15} {da:<50} {ms:<50}'.format(
		st = std, d = date, ti = time, f = 'File: '+ filePath, ln = 'Line: ' + str(line), ms = 'message: ' + message, da = 'data: ' + data, ty = data_type))
	conn.commit()


def endLog():
	conn = sqlite3.connect('log.db')
	c = conn.cursor()
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d")
	time = now.strftime('%H:%M:%S')
	ms = 'terminated'
	c.execute('INSERT INTO log VALUES(?,?,?,?,?,?,?,?)', (ms, date, time, ms, ms, ms, ms, ms))
	conn.commit()
