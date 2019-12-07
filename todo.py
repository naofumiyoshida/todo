#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sqlite3

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
cgitb.enable()

print("Content-type: text/html; charset=utf-8")
print("Pragma: no-cache")
print("Cache-Control: no-cache")
print()
print('''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=UTF-8">
<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
<title>python message board</title>

<style type="text/css">
body {
    color: black;
	background-color: white;
	}
</style>

</head>
<body>

<form method="POST" action="./todo.py">
<table>
<tr>
  <td><b>ToDo</b></td>
  <td><input type="text" name="item" size="20" value=""></td>
</tr>
<tr>
  <td colspan="2"><input type="submit" value="Save"><input type="reset" value="Reset"></td>
</tr>
</table>
</form>
''')


con = sqlite3.connect("todo.db")
try:
  # Database Creation
  con.executescript("""create table todo(item text, id INTEGER PRIMARY KEY AUTOINCREMENT);""")
except sqlite3.Error as e:
  #print('sqlite3.Error occurred:', e.args[0])
  print
finally:
  # If there is input, insert data to database
  form = cgi.FieldStorage()
  #  print( form["name"].value )
  if "item" in form:
    # if name is specified, insert data
    item = form["item"].value

    cur = con.cursor()
    try:
      cur.execute("insert into todo(item) values('"+(cgi.escape(item))+"')")
      con.commit()
    except sqlite3.Error as e:
      print('sqlite3.Error occurred:', e.args[0])
      con.rollback()
    finally:
      cur.close()

  # display messages
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  try:
    cur.execute("select * from todo")
    print("<table border=1>")
    for each in cur.fetchall():
      print('<tr>')
      print('<td>', each['item'], '</td>')
      print('<td><a href="tododelete.py?id=',each['id'] , '">delete</a></td>',sep='')
      print('</tr>')
    print("</table>")
  except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])
  finally:
    cur.close()
  con.close()
  print("</body></html>")
