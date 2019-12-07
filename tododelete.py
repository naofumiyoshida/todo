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
<meta http-equiv="refresh" content="5;URL='http://gmsresearch01.komazawa-u.ac.jp/~naofumi/todo.py'" />
<title>python message board</title>

<style type="text/css">
body {
    color: black;
	background-color: white;
	}
</style>

</head>
''')

con = sqlite3.connect("todo.db")
form = cgi.FieldStorage()
id = form["id"].value
cur = con.cursor()
try:
    print("deleting...<br>")
    sql="delete from todo where id='"+(cgi.escape(id))+"'"
    print(sql)
    print("<p></p>")
    cur.execute(sql)
    con.commit()
except:
    con.rollback()
finally:
    cur.close()
    print("<a href=todo.py>back</a>")

con.close()
print("</body></html>")
