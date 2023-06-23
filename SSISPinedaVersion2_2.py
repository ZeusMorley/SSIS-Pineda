from tkinter import *
import tkinter as tk
import sqlite3

root = tk.Tk()
root.title('SSIS V2 PINEDA')
root.geometry("460x640")
root.resizable(width=False, height=False)
root.configure(bg='#252525')

conn = sqlite3.connect('SSIS_Pineda.db')
c = conn.cursor()

# Custom things -----------------------------------
class CustomRadiobutton(tk.Radiobutton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure the background color of the circle
        self.config(selectcolor='#252525')

# Header and Footer ----------------------------------
header_title = Label(root, text="SSIS", 
	font=('Arial',24), fg='white', bg='#35d17c')
header_title.grid(row=0, column=0, columnspan=6, ipadx=200)
global course_list
course_list = []
# Creating Tables
'''
c.execute("""CREATE TABLE students(
		first_name text,
		middle_name text,
		last_name text,
		id_number text,
		gender text,
		year_level integer,
		course_code text
		)""")
c.execute("""CREATE TABLE courses(
		course_code text,
		course_name text
		)""")
'''


# Functions -------------------------------------------------------
def refresh_courses():
	global course 
	courses_list = []
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()
	c.execute("SELECT course_code FROM courses")

	course_list = c.fetchall()
	course = StringVar()
	course.set(course_list[0])
	courses_listed = OptionMenu(root, course, *course_list)
	courses_listed.config(width=10)
	courses_listed.grid(row=7, column=1)

	conn.commit()
	conn.close()
def course_search():
	search_list = Tk()
	search_list.title('SEARCH RESULTS')
	search_list.geometry("300x300")
	search_list.resizable(width=False, height=False)
	search_list.configure(bg='#252525')

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	search = select_course.get()
	query = "SELECT * FROM courses WHERE course_code = ?"
	c.execute(query, (search,))
	records = c.fetchall()

	if records:
		print(records)
		print_records = ''

		for record in records:
			course_code = record[0]
			course_name = record[1]

			print_records += str(record[0]) + " - " + str(record[1]) + "\n"

		list_label = Label(search_list, text=print_records,
		font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525').pack()


	else:
		Label(search_list, text="NO COURSE FOUND",
		font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525').pack()

	conn.commit()
	conn.close()

	select_course.delete(0,END)
def edit_course():
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT * FROM courses WHERE oid= " + select_course.get())

	records = c.fetchall()

	for record in records:
		course_code.insert(0, record[0])
		course_name.insert(0, record[1])

	# Add Course Button
	add_course_btn = Button(root, text="CONFIRM EDIT",
	font=('Arial', 10, 'bold'), fg='white', bg='#35d17c', command=add_course)
	add_course_btn.grid(row=18, column=1, ipadx=40, padx=(1,0))

	c.execute("DELETE from courses WHERE oid= " + select_course.get())
	select_course.delete(0,END)

	refresh_courses()

	conn.commit()
	conn.close()

def delete_course():
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("DELETE from courses WHERE oid= " + select_course.get())
	select_course.delete(0,END)

	refresh_courses()
	conn.commit()
	conn.close()

def list_courses():
	courses_list = Tk()
	courses_list.title('LIST OF COURSES')
	courses_list.geometry("300x300")
	courses_list.resizable(width=False, height=False)
	courses_list.configure(bg='#252525')

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT *, oid FROM courses")
	records = c.fetchall()
	print(records)

	print_records = ''
	for record in records:
		print_records += str(record[2]) + "  -  (" + str(record[0]) + ") " +str(record[1]) + "\n"

	list_label = Label(courses_list, text=print_records,
		font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525').pack()

	conn.commit()
	conn.close()

def add_course():
	# Add Course Button
	add_course_btn = Button(root, text="ADD COURSE",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=add_course)
	add_course_btn.grid(row=18, column=1, ipadx=44, padx=(1,0))

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("INSERT INTO courses VALUES(:course_code, :course_name)",
			{
				'course_code': course_code.get(),
				'course_name': course_name.get()
			})
	conn.commit()
	conn.close()

	refresh_courses()

	course_code.delete(0,END)
	course_name.delete(0,END)

def student_search():
	search_list = Tk()
	search_list.title('SEARCH RESULTS')
	search_list.geometry("300x300")
	search_list.resizable(width=False, height=False)
	search_list.configure(bg='#252525')

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	search = search_student.get()
	query = "SELECT * FROM students WHERE last_name = ?"
	c.execute(query, (search,))
	records = c.fetchall()

	if records:
		print(records)
		print_records = ''

		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2]

			print_records += str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n"

		list_label = Label(search_list, text=print_records,
		font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525').pack()
	else:
		conn = sqlite3.connect('SSIS_Pineda.db')
		c = conn.cursor()

		search = search_student.get()
		query = "SELECT * FROM students WHERE id_number = ?"
		c.execute(query, (search,))
		records = c.fetchall()

		if records:
			print(records)
			print_records = ''

			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]
				id_number = record[3]

				print_records += str(record[3]) + " - " + str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n"

			list_label = Label(search_list, text=print_records,
			font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525').pack()

		else:
			Label(search_list, text="NO STUDENT FOUND",
			font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525').pack()
	conn.commit()
	conn.close()

def student_keys():
	students_key_list = Tk()
	students_key_list.title('STUDENT KEYS')
	students_key_list.geometry("240x700")
	students_key_list.resizable(width=False, height=False)
	students_key_list.configure(bg='#252525')

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()
	c.execute("SELECT *, oid FROM students")
	records = c.fetchall()
	print(records)

	print_records = ''
	for record in records:
		print_records += str(record[7]) + " - " + str(record[2]) + ", " + str(record[0]) + " " + str(record[1]) + "\n"

	list_label = Label(students_key_list, text=print_records,
		font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()

	conn.commit()
	conn.close()

def delete_student():
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()
	c.execute("DELETE from students WHERE oid= " + select_student.get())

	select_student.delete(0,END)
	conn.commit()
	conn.close()

def edit_student():
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()
 
	c.execute("SELECT * FROM students WHERE oid= " + select_student.get())
	records = c.fetchall()

	for record in records:
		f_name.insert(0, record[0])
		m_name.insert(0, record[1])
		l_name.insert(0, record[2])
		id_num.insert(0, record[3])
		gender.set(value=record[4])
		yearlvl.set(value=record[5])
		course.set(value=record[6])

	# Submit Button
	submit_btn = Button(root, text="CONFIRM EDIT", command=submit,
		font=('Arial', 10, 'bold'), fg='white', bg='#35d17c')
	submit_btn.grid(row=8, column=1, columnspan=2, pady=10, padx=(0,18), ipadx=40)

	c.execute("DELETE from students WHERE oid= " + select_student.get())
	select_student.delete(0,END)

	conn.commit()
	conn.close()

def list_down_students():
	students_list = Tk()
	students_list.title('LIST OF STUDENTS')
	students_list.geometry("500x700")
	students_list.resizable(width=False, height=False)
	students_list.configure(bg='#252525')

	formats=choice.get()
	print(formats)
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	if formats == "SORTED BY NAME":
		c.execute("SELECT * FROM students ORDER BY last_name")
		records = c.fetchall()

		print_records = ''
		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			course_code = record[6]
			print_records += str(record[2]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n"

		list_label = Label(students_list, text=print_records,
			font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()
	elif formats == "SORTED BY ID NUMBER":
		c.execute("SELECT * FROM students ORDER BY id_number")
		records = c.fetchall()

		print_records = ''
		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			course_code = record[6]
			print_records += str(record[3]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[4]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n"

		list_label = Label(students_list, text=print_records,
			font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()
	elif formats == "SORTED BY GENDER":
		c.execute("SELECT * FROM students ORDER BY gender")
		records = c.fetchall()

		print_records = ''
		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			course_code = record[6]
			print_records += str(record[4]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n"

		list_label = Label(students_list, text=print_records,
			font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()
	elif formats == "SORTED BY YEAR LEVEL":
		c.execute("SELECT * FROM students ORDER BY year_level")
		records = c.fetchall()

		print_records = ''
		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			course_code = record[6]
			print_records += str(record[5]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[6]) + "\n"

		list_label = Label(students_list, text=print_records,
			font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()
	elif formats == "SORTED BY COURSE":
		c.execute("SELECT * FROM students ORDER BY course_code")
		records = c.fetchall()

		print_records = ''
		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			course_code = record[6]
			print_records += str(record[6]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + "\n"

		list_label = Label(students_list, text=print_records,
			font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()
	else:
		c.execute("SELECT *, oid FROM students")
		records = c.fetchall()
		print(records)

		print_records = ''
		for record in records:
			print_records += str(record[7]) + " - " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n"

		list_label = Label(students_list, text=print_records,
			font=('Arial', 7, 'bold'), fg='#35d17c', bg='#252525').pack()
	conn.commit()
	conn.close()

def submit():
	global gender
	global yearlvl
	global course

	# Submit Button
	submit_btn = Button(root, text="ADD STUDENT", command=submit,
		font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c')
	submit_btn.grid(row=8, column=1, columnspan=2, pady=10, padx=(0,18), ipadx=40)
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("INSERT INTO students VALUES(:f_name, :m_name, :l_name, :id_num, :gender, :yearlvl, :course)",
			{
				'f_name': f_name.get(),
				'm_name': m_name.get(),
				'l_name': l_name.get(),
				'id_num': id_num.get(),
				'gender': gender.get(),
				'yearlvl': yearlvl.get(),
				'course': course.get()
			})
	conn.commit()
	conn.close()

	f_name.delete(0,END)
	m_name.delete(0,END)
	l_name.delete(0,END)
	id_num.delete(0,END)

# Text Boxes -------------------------------------------------------
f_name = Entry(root, width=30, fg='white', bg='#252525')
f_name.grid(row=1, column=1, padx=20, pady=(10,0))

m_name = Entry(root, width=30, fg='white', bg='#252525')
m_name.grid(row=2, column=1, padx=20)

l_name = Entry(root, width=30, fg='white', bg='#252525')
l_name.grid(row=3, column=1, padx=20)

id_num = Entry(root, width=30, fg='white', bg='#252525')
id_num.grid(row=4, column=1, padx=20)

gender = StringVar(value="None")
male_gender = CustomRadiobutton(root, text="MALE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525', variable=gender, value="MALE")
male_gender.grid(row=5, column=1, padx=(0,130))
female_gender = CustomRadiobutton(root, text="FEMALE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525', variable=gender, value="FEMALE")
female_gender.grid(row=5, column=1, padx=(115,0))

yearlvl = StringVar(value="None")
first = CustomRadiobutton(root, text='1',
	font=('Arial', 8, 'bold'), fg='#35d17c', bg='#252525', variable=yearlvl, value=1)
first.grid(row=6, column=1, padx=(0,160))

second = CustomRadiobutton(root, text='2',
	font=('Arial', 8, 'bold'), fg='#35d17c', bg='#252525', variable=yearlvl, value=2)
second.grid(row=6, column=1, padx=(0,55))

third = CustomRadiobutton(root, text='3',
	font=('Arial', 8, 'bold'), fg='#35d17c', bg='#252525', variable=yearlvl, value=3)
third.grid(row=6, column=1, padx=(55,0))

fourth = CustomRadiobutton(root, text='4',
	font=('Arial', 8, 'bold'), fg='#35d17c', bg='#252525', variable=yearlvl, value=4)
fourth.grid(row=6, column=1, padx=(160,0))

refresh_courses()

global choice
choice_list = [
	"UNSORTED",
	"SORTED BY NAME",
	"SORTED BY ID NUMBER",
	"SORTED BY GENDER",
	"SORTED BY YEAR LEVEL",
	"SORTED BY COURSE",
]
choice = StringVar()
choice.set(choice_list[0])
choices_listed = OptionMenu(root, choice, *choice_list)
choices_listed.config(width=20)
choices_listed.grid(row=9, column=1)

select_student = Entry(root, width=30, fg='white', bg='#252525')
select_student.grid(row=11, column=1, padx=20)

search_student = Entry(root, width=30, fg='white', bg='#252525')
search_student.grid(row=14, column=1, padx=20, pady=5)

course_name = Entry(root, width=30, fg='white', bg='#252525')
course_name.grid(row=16, column=1, padx=20, pady=(5,2))

course_code = Entry(root, width=30, fg='white', bg='#252525')
course_code.grid(row=17, column=1, padx=20)

select_course = Entry(root, width=30, fg='white', bg='#252525')
select_course.grid(row=19, column=1, padx=20, pady=(5,0))

# Text Box Labels -------------------------------------------------------

f_name_label = Label(root, text="FIRST    NAME", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
f_name_label.grid(row=1,column=0, pady=(10,0))

m_name_label = Label(root, text="MIDDLE NAME", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
m_name_label.grid(row=2,column=0)

l_name_label = Label(root, text="LAST     NAME",
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
l_name_label.grid(row=3,column=0)

id_num_label = Label(root, text="ID NUMBER",
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
id_num_label.grid(row=4,column=0)

gender_label_add = Label(root, text="GENDER",
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
gender_label_add.grid(row=5,column=0)

yearlvl_label_add = Label(root, text="YEAR LEVEL",
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
yearlvl_label_add.grid(row=6,column=0)

course_list_label = Label(root, text="COURSE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
course_list_label.grid(row=7,column=0)

student_list_down_label = Label(root, text="STUDENT LIST", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
student_list_down_label.grid(row=9,column=0)

select_student_label = Label(root, text="INPUT STUDENT KEY", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
select_student_label.grid(row=11,column=0)

search_student_label = Label(root, text="INPUT LAST NAME/ID #", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
search_student_label.grid(row=14,column=0)

add_course_name_label = Label(root, text="COURSE NAME", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
add_course_name_label.grid(row=16,column=0)

add_course_code_label = Label(root, text="COURSE CODE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
add_course_code_label.grid(row=17,column=0)

edit_select_delete_label = Label(root, text="EDIT DELETE SEARCH", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
edit_select_delete_label.grid(row=19,column=0, pady=(2,0))

select_course_key_label = Label(root, text="INPUT COURSE KEY #", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
select_course_key_label.grid(row=20,column=0, pady=(2,0))

select_course_code_label = Label(root, text="INPUT COURSE CODE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
select_course_code_label.grid(row=21,column=0, pady=(2,0))

# Submit Button
submit_btn = Button(root, text="ADD STUDENT", command=submit,
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c')
submit_btn.grid(row=8, column=1, columnspan=2, pady=10, padx=(0,14), ipadx=40)

# Lists Button
lists_btn = Button(root, text="LIST STUDENTS",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=list_down_students)
lists_btn.grid(row=10, column=1, pady=10, ipadx=35)

# Delete Button
delete_btn = Button(root, text="DELETE",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=delete_student)
delete_btn.grid(row=12, column=1, padx=(93,0), ipadx=16)

# Edit Button
edit_btn = Button(root, text="EDIT",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=edit_student)
edit_btn.grid(row=12, column=1, padx=(0,93), ipadx=25, pady=2)

# Student Key List Button
delete_btn = Button(root, text="STUDENT KEYS",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=student_keys)
delete_btn.grid(row=12, column=0)

# Search student Button
search_btn = Button(root, text="SEARCH STUDENT",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=student_search)
search_btn.grid(row=15, column=1, ipadx=28)

# Add Course Button
add_course_btn = Button(root, text="ADD COURSE",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=add_course)
add_course_btn.grid(row=18, column=1, ipadx=44, padx=(1,0))

# Course List Button
course_list_btn = Button(root, text="LIST COURSES",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=list_courses)
course_list_btn.grid(row=18, column=0)

# Course Delete Button
course_delete_btn = Button(root, text="DELETE", command=delete_course,
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c')
course_delete_btn.grid(row=20, column=1,padx=(93,0), ipadx=16, pady=2)

# Course Edit Button
course_edit_btn = Button(root, text="EDIT", command=edit_course,
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c')
course_edit_btn.grid(row=20, column=1, padx=(0,93), ipadx=25)

# Course Edit Button
course_search_btn = Button(root, text="SEARCH COURSE", command=course_search,
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c')
course_search_btn.grid(row=21, column=1, ipadx=31, padx=(1,0))

conn.commit()
conn.close()
root.mainloop()

'''
def list_courses():
	def update_list_position(value):
		position = int(value)
		listbox.yview_moveto(position / 100)

	courses_list = Tk()
	courses_list.title('LIST OF COURSES')
	courses_list.geometry("300x300")
	courses_list.resizable(width=False, height=False)
	courses_list.configure(bg='#252525')

	listbox = tk.Listbox(courses_list)
	listbox.pack()

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT *, oid FROM courses")
	records = c.fetchall()

	for record in records:
		listbox.insert(tk.END, records)

	# Create a slider
	slider = tk.Scale(courses_list, from_=0, to=100, orient=tk.VERTICAL, command=update_list_position)
	slider.pack()

	conn.commit()
	conn.close()
'''