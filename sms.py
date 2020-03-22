import cx_Oracle
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from ttkthemes import ThemedTk 
from tkinter import ttk
import socket
import requests 
import bs4
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import winsound

def show_add():
	addst.deiconify()
	root.withdraw()

def back():
	addst.withdraw()
	vist.withdraw()
	upst.withdraw()
	delst.withdraw()
	grst.withdraw()
	root.deiconify()

def show_upd():
	upst.deiconify()
	root.withdraw()

def show_del():
	delst.deiconify()
	root.withdraw()

def show_graph():
	grst.deiconify()
	root.withdraw()

def show_view():
	vist.deiconify()
	root.withdraw()
	con = None
	try:
		stdata.delete(1.0, END)
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		
		msg = ''
		for d in data:
			msg = msg + "Rno : " + str(d[0]) + "\n  Name : " + d[1] + "\n  Marks : " + str(d[2]) + '\n'+( '*'*42 )+ '\n' 
		stdata.insert(INSERT, msg)
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("issue : ",e)
	except Exception as e :
		print("Exception", e)
	finally :
		if con is not None:
			con.close()

def num_there(s):
	return any(i.isdigit() for i in s)

def add_stu():
	con = None
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		all1 = 'select rno from student'
		cursor.execute(all1)
		rno_list = cursor.fetchall()
		rno = int(rnoety.get())
		flag1 = True
		flag2 = True
		flag3 = True
		if (rno,) in rno_list:
			winsound.Beep(200,1000)
			messagebox.showerror("Error","Roll Number Already Exists")
			rnoety.delete(0, END)
			flag1 = False
			rnoety.focus_set()
		else:
			flag1 = True
		name = nameety.get()
		if num_there(name):
			winsound.Beep(200,1000)
			messagebox.showerror("Error", "Name cannot contain Digits")
			nameety.delete(0, END)
			flag2 = False
			nameety.focus_set()
		else:
			flag2 = True
		mks = int(mksety.get())
		if not 0<=mks<=100:
			flag3 = False 
			winsound.Beep(200,1000)
			messagebox.showerror("Error", "Invalid Marks")
			mksety.delete(0, END)
			mksety.focus_set()
		else:
			flag3 = True
		if flag1 and flag2 and flag3:
			sql = "insert into student values ('%d','%s', '%d')"
			args = (rno,name,mks)
			cursor.execute(sql%args)
			con.commit()
			pygame.mixer.music.play()
			time.sleep(2)
			pygame.mixer.music.stop()
			messagebox.showinfo("Success","Records inserted")
	except Exception as e:
		con.rollback()
	finally :
		if flag1 and flag2 and flag3 :
			rnoety.delete(0, END)
			nameety.delete(0, END)
			mksety.delete(0, END)
		if con is not None:
				con.close()

def upd_stu():
	con = None
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		all1 = 'select rno from student'
		cursor.execute(all1)
		rno_list = cursor.fetchall()
		rno = int(rnoety1.get())
		flag1, flag2, flag3 = True, True, True
		if (rno,) not in rno_list:
			winsound.Beep(200,1000)
			messagebox.showerror("Error","Roll Number Does Not Exist")
			rnoety1.delete(0, END)
			flag1 = False
			rnoety1.focus_set()
		else:
			flag1 = True
		name = nameety1.get()
		if num_there(name):
			winsound.Beep(200,1000)
			messagebox.showerror("Error","Name cannot contain Digits")
			nameety1.delete(0, END)
			nameety1.focus_set()
			flag2 = False
		else:
			flag2 = True
		mks = int(mksety1.get())
		if not 0 <= mks <= 100:
			flag3 = False
			winsound.Beep(200,1000)
			messagebox.showerror("Error","Invalid Marks")
			mksety1.delete(0, END)
			mksety1.focus_set()
		else:
			flag3 = True
		if flag1 and flag2 and flag3:
			sql = "update student set name = '%s' , mks = '%d' where rno like '%d'"
			args = (name, mks, rno)
			cursor.execute(sql % args)
			con.commit()
			pygame.mixer.music.play()
			time.sleep(2)
			pygame.mixer.music.stop()
			messagebox.showinfo("Success","Record Updated")
	except cx_Oracle.DatabaseError as e:
		con.rollback()
	finally:
		if flag1 and flag2 and flag3:
			rnoety1.delete(0, END)
			nameety1.delete(0, END)
			mksety1.delete(0, END)
		if con is not None:
			con.close()

def del_stu():
	delst.deiconify()
	root.withdraw()
	con = None
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		all1 = 'select rno from student'
		cursor.execute(all1)
		rno_list = cursor.fetchall()
		rno = int(rnoety2.get())
		if (rno,) in rno_list:
			sql = "delete from student where rno like ('%d')"
			args = (int(rnoety2.get()))
			cursor.execute(sql%args)
			con.commit()
			pygame.mixer.music.play()
			time.sleep(2)
			pygame.mixer.music.stop()
			messagebox.showinfo("Success","Record Successfully Deleted")
		else:
			winsound.Beep(200,1000)
			messagebox.showerror("Error","Roll No not in Record")
			rnoety2.delete(0,END)
			rnoety2.focus_set()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("issue : ",e)
	finally :
		if con is not None:
			con.close()

def bargraph():
	con = None
	grst.withdraw()
	root.deiconify()
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		all1 = 'select * from student'
		cursor.execute(all1)
		data = cursor.fetchall()
		rollno = []
		marks = []
		for i in data:
			rollno.append(i[0])
			marks.append(i[2])
		plt.bar(rollno , marks, color = 'red', alpha = 0.5)
		plt.xlabel("Roll Number")
		plt.ylabel("Marks")
		plt.grid()
		plt.title("PERFOMANCE")
		plt.show()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("issue : ",e)
	finally :
		if con is not None:
			con.close()

def linegraph():
	con = None
	grst.withdraw()
	root.deiconify()
	try:
		con = cx_Oracle.connect('system/abc123')
		cursor = con.cursor()
		all1 = 'select * from student'
		cursor.execute(all1)
		data = cursor.fetchall()
		rollno = []
		marks = []
		for i in data:
			rollno.append(i[0])
			marks.append(i[2])
		plt.plot(rollno , marks, marker = 'o', markersize = 10)
		plt.xlabel("NAME")
		plt.ylabel("MARKS")
		plt.title("PERFOMANCE")
		plt.grid()
		plt.show()
	except cx_Oracle.DatabaseError as e:
		messagebox.showerror("issue : ",e)
	finally :
		if con is not None:
			con.close() 


pygame.mixer.init()
success = pygame.mixer.music.load('success.mp3')


root = ThemedTk(theme = 'radiance')
root.title("Student Management System")
root.geometry("300x400+200+100")
mainlbl = ttk.Label(root, text = "Student Management System", justify = CENTER)
mainlbl.pack(pady = 5)
addbtn = ttk.Button(root, text = "Add", command = show_add, width = 20)
addbtn.pack(pady = 5)
viewbtn = ttk.Button(root, text = "View", command = show_view, width = 20)
viewbtn.pack(pady = 5)
updbtn = ttk.Button(root, text = "Update", command = show_upd, width = 20)
updbtn.pack(pady = 5)
delbtn = ttk.Button(root, text = "Delete", command = show_del, width = 20)
delbtn.pack(pady = 5)
graphbtn = ttk.Button(root, text = "Graph", command = show_graph, width = 20)
graphbtn.pack(pady = 5)
try:
	socket.create_connection(("google.com",80))
	res = requests.get("http://ipinfo.io")
	city = res.json()['city']
	res1 = requests.get("http://api.openweathermap.org/data/2.5/weather?units=metric&q="+city+"&appid=37b53ff5a9b9d32307f63fe99f8c4692")
	res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	quote = soup.find('img', {'class' : 'p-qotd'})
	qt = quote['alt']
	temp = res1.json()['main']['temp']
	temp = "Temp : " + str(temp) +"°C"
except OSError as e:
	messagebox.showerror("Connectivity Issue", "Please Check Internet Connection")
	city, temp, qt = "","",""
except KeyError:
	temp  = ''
qtlbl = ttk.Label(root, text = qt, justify = CENTER, wraplength = 250)
qtlbl.pack(pady = 10)
citylbl = ttk.Label(root, text = "City : "+city)
citylbl.pack(side = LEFT,  padx = 5, ipadx = 5)
templbl = ttk.Label(root, text = temp)
templbl.pack(side = RIGHT , padx = 5, ipadx = 5)

addst = Toplevel(root)
addst.title("Add Student")
addst.geometry("300x400+200+100")
addst.withdraw()
rnolbl = ttk.Label(addst, text = "Enter Roll No")
rnolbl.pack(pady = 10)
rnoety = ttk.Entry(addst)
rnoety.pack(pady = 10)
namelbl = ttk.Label(addst, text = "Enter Name")
namelbl.pack(pady = 10)
nameety = ttk.Entry(addst)
nameety.pack(pady = 10)
mkslbl = ttk.Label(addst, text = "Enter Marks")
mkslbl.pack(pady = 10)
mksety = ttk.Entry(addst)
mksety.pack(pady = 10)
savebtn = ttk.Button(addst, text = "Save", command = add_stu, width = 15)
savebtn.pack(pady = 10)
backbtn = ttk.Button(addst, text = "Back", command = back, width = 15)
backbtn.pack(pady = 10)

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("300x400+200+100")
vist.withdraw()
stdata = scrolledtext.ScrolledText(vist, height = 20, width = 32, font = "TkDefaultFont")
stdata.pack(pady = 5)
backbtn = ttk.Button(vist, text = "Back", command = back, width = 15)
backbtn.pack(pady = 5)

upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("300x400+200+100")
upst.withdraw()
rnolbl1 = ttk.Label(upst, text = "Enter Roll No")
rnolbl1.pack(pady = 10)
rnoety1 = ttk.Entry(upst)
rnoety1.pack(pady = 10)
namelbl1 = ttk.Label(upst, text = "Enter Name")
namelbl1.pack(pady = 10)
nameety1 = ttk.Entry(upst)
nameety1.pack(pady = 10)
mkslbl1 = ttk.Label(upst, text = "Enter Marks")
mkslbl1.pack(pady = 10)
mksety1 = ttk.Entry(upst)
mksety1.pack(pady = 10)
savebtn1 = ttk.Button(upst, text = "Save" ,command = upd_stu, width = 15)
savebtn1.pack(pady = 10)
backbtn1 = ttk.Button(upst, text = "Back", command = back, width = 15)
backbtn1.pack(pady = 10)

delst = Toplevel(root)
delst.title("Delete Student")
delst.geometry("300x400+200+100")
delst.withdraw()
rnolbl = ttk.Label(delst, text = "Enter Roll No")
rnolbl.pack(pady = 10)
rnoety2 = ttk.Entry(delst)
rnoety2.pack(pady = 10)
savebtn = ttk.Button(delst, text = "Remove", command = del_stu, width = 15)
savebtn.pack(pady = 10)
backbtn = ttk.Button(delst, text = "Back", command = back, width = 15)
backbtn.pack(pady = 100)

grst = Toplevel(root)
grst.title("Graphs")
grst.geometry("300x400+200+100")
grst.withdraw()
grlbl = ttk.Label(grst, text = "Select Type Of Graph")
grlbl.pack(pady = 10)
barbtn = ttk.Button(grst, text = "Bar Graph", command = bargraph,  width = 20)
barbtn.pack(pady = 10)
linebtn = ttk.Button(grst, text = "Line Graph", command = linegraph, width = 20)
linebtn.pack(pady = 10)
bckbtn = ttk.Button(grst, text = "Back", command = back, width = 15)
bckbtn.pack(pady = 90)

root.mainloop()