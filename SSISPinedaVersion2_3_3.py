from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import messagebox

root = tk.Tk()
root.title('SSIS V2 PINEDA')
root.geometry("460x600")
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
# Creating Tables
'''
c.execute("""CREATE TABLE students(
		first_name text,
		middle_name text,
		last_name text,
		id_number text,
		gender text,
		year_level text,
		s_course_code text
		)""")
c.execute("""CREATE TABLE courses(
		course_code text,
		course_name text
		)""")
'''


# Functions -------------------------------------------------------
def check_course_code_exists():
	first = f_name.get()
	middle = m_name.get()
	last = l_name.get()
	num = id_num.get()
	gen = gender.get()
	yr = yearlvl.get()
	crs = course.get()

	if first.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	if middle.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	if last.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	if num.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	if gen.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	if yr.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	if crs.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	check_course = course.get()
	query = "SELECT * FROM courses WHERE course_code = ?"
	c.execute(query, (check_course,))
	records = c.fetchall()

	if records:
		check_students_id_duplicate()
	else:
		messagebox.showerror("Course Code Error", "Course Code does not exist in the Course List, \nPlease input a Course Code from the Course list")

	conn.commit()
	conn.close()

def check_course_code_duplicate():
	check_code = course_code.get()
	check_name = course_name.get()

	if check_code.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return
	if check_name.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	query = "SELECT * FROM courses WHERE course_code = ?"
	c.execute(query, (check_code,))
	records = c.fetchall()

	if records:
		messagebox.showerror("Course Code Duplicate Error", "Course Code already exists in the Course List, \nPlease input a different Course Code.")

	else:
		add_course()

	conn.commit()
	conn.close()

def check_students_id_duplicate():
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	check_id = id_num.get()
	query = "SELECT * FROM students WHERE id_number = ?"
	c.execute(query, (check_id,))
	records = c.fetchall()

	if records:
		messagebox.showerror("ID Number Error", "The ID number already exists among the students, \nPlease input a different ID number")
	else:
		submit()

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
	c.execute("SELECT * FROM courses WHERE course_code LIKE ?", ('%' + search + '%',))
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
		search = select_course.get()
		c.execute("SELECT * FROM courses WHERE course_name LIKE ?", ('%' + search + '%',))
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
	search = select_course.get()
	if search.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return
	# Disable course code entry box
	course_code.grid_forget()

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT * FROM courses WHERE oid= " + select_course.get())

	records = c.fetchall()

	for record in records:
		course_code.insert(0, record[0])
		course_name.insert(0, record[1])

	# Add Course Button
	add_course_btn = Button(root, text="CONFIRM EDIT",
	font=('Arial', 10, 'bold'), fg='white', bg='#35d17c', command=check_course_code_duplicate)
	add_course_btn.grid(row=18, column=1, ipadx=40, padx=(1,0))

	c.execute("DELETE from courses WHERE oid= " + select_course.get())
	select_course.delete(0,END)

	conn.commit()
	conn.close()

def delete_course():
	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	search = select_course.get()
	if search.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return
		
	holder = ''

	query = "SELECT * FROM courses WHERE oid= ?"
	c.execute(query, (search,))

	records = c.fetchall()
	for record in records:
		holder = record[0] # Course code
	
	c.execute("SELECT * FROM students WHERE s_course_code=?", (holder,))
	result = c.fetchone()

	if result:
		messagebox.showerror("Course Delete Error", "This Course contains a student, \nYou can only delete an empty course (no students enrolled)")

	else:
		c.execute("DELETE from courses WHERE oid= " + search)
		select_course.delete(0,END)

	conn.commit()
	conn.close()

def list_courses():
	courses_list = Tk()
	courses_list.title('LIST OF COURSES')
	courses_list.geometry("400x300")
	courses_list.resizable(width=False, height=False)
	courses_list.configure(bg='#252525')

	listbox = tk.Listbox(courses_list, width=70)
	listbox.config(font=('Arial', 12, 'bold'),bg='#252525', fg='#35d17c')
	listbox.pack(side=tk.LEFT, fill=tk.BOTH)

	scrollbar = tk.Scrollbar(courses_list)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	listbox.config(yscrollcommand=scrollbar.set)
	scrollbar.config(command=listbox.yview)

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT *, oid FROM courses")
	records = c.fetchall()
	
	for record in records:
		listbox.insert(tk.END, str(record[2]) + "  -  (" + str(record[0]) + ") " +str(record[1]) + "\n") 

	conn.commit()
	conn.close()

def add_course(): # add error if duplicate course code input
	# Enable coursecode Entry box
	course_code.grid(row=17, column=1, padx=20)

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

	course_code.delete(0,END)
	course_name.delete(0,END)

def student_search():
	search = search_student.get()
	if search.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	counter = 0
	search_list = Tk()
	search_list.title('SEARCH RESULTS')
	search_list.geometry("600x400")
	search_list.resizable(width=False, height=False)
	search_list.configure(bg='#252525')

	listbox = tk.Listbox(search_list, width=80)
	listbox.config(font=('Arial', 12, 'bold'))
	listbox.config(bg='#252525', fg='#35d17c')
	listbox.pack(side=tk.LEFT, fill=tk.BOTH)

	scrollbar = tk.Scrollbar(search_list)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	listbox.config(yscrollcommand=scrollbar.set)
	scrollbar.config(command=listbox.yview)

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()
	
	listbox.insert(tk.END, "You searched for: " + search)
	listbox.insert(tk.END, "")
		
	if search == "FEMALE":
		c.execute("SELECT * FROM students WHERE gender LIKE ?", ('%' + "F" + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Genders match -----")

			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]
				gender = record[4]
				listbox.insert(tk.END, str(record[4]) + " | " + str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of Genders match -----")
			listbox.insert(tk.END, "")

	elif search == "MALE":
		c.execute("SELECT * FROM students WHERE gender NOT LIKE ?", ('%' + "F" + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Genders match -----")

			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]
				gender = record[4]

				listbox.insert(tk.END, str(record[4]) + " | " + str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of Genders match -----")
			listbox.insert(tk.END, "")

	else:
		c.execute("SELECT * FROM students WHERE first_name LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ First name match -----")
			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]

				listbox.insert(tk.END, str(record[0]) + " | " + str(record[1]) + " " + str(record[2]) + "\n")
			listbox.insert(tk.END, "------END of First name match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM students WHERE middle_name LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Middle name match -----")
			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]

				listbox.insert(tk.END, str(record[1]) + " | " + str(record[0]) + " " + str(record[2]) + "\n")
			listbox.insert(tk.END, "------END of Middle name match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM students WHERE last_name LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Last name match -----")
			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]

				listbox.insert(tk.END, str(record[2]) + " | " + str(record[0]) + " " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of Last name match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM students WHERE id_number LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ ID number match -----")
			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]
				id_number = record[3]

				listbox.insert(tk.END, str(record[3]) + " | " + str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of ID number match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM students WHERE year_level LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Year Level match -----")
			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]
				year_level = record[5]

				listbox.insert(tk.END, str(record[5]) + " | " + str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of Year Level match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM students WHERE s_course_code LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------Student Course Code match -----")
			for record in records:
				first_name = record[0]
				middle_name = record[1]
				last_name = record[2]
				s_course_code = record[6]

				listbox.insert(tk.END, str(record[6]) + " | " + str(record[2]) + " " + str(record[0]) + " " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of Student Course Code match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM courses WHERE course_code LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Course Codes match -----")
			for record in records:
				course_code = record[0]
				course_name = record[1]

				listbox.insert(tk.END, str(record[0]) + " | " + str(record[1]) + "\n")
			listbox.insert(tk.END, "------END of Course Codes match -----")
			listbox.insert(tk.END, "")

		c.execute("SELECT * FROM courses WHERE course_name LIKE ?", ('%' + search + '%',))
		records = c.fetchall()

		if records:
			counter+=1
			listbox.insert(tk.END, "------ Course Names match -----")
			for record in records:
				course_code = record[0]
				course_name = record[1]

				listbox.insert(tk.END, str(record[0]) + " | " + str(record[1]) + "\n")

				c.execute("SELECT * FROM students WHERE s_course_code LIKE ?", ('%' + record[0] + '%',))
				records2 = c.fetchall()

				if records2:
					counter+=1
					listbox.insert(tk.END, "")
					listbox.insert(tk.END, "------" + record[1] + " match in Students-----")
					for record2 in records2:
						first_name = record2[0]
						middle_name = record2[1]
						last_name = record2[2]
						s_course_code = record2[6]

						listbox.insert(tk.END, "> " + str(record[1]) + " | " + str(record2[2]) + " " + str(record2[0]) + " " + str(record2[1]) + "\n")
					listbox.insert(tk.END, "------ END of " + record[1] + " match in Students -----")
					listbox.insert(tk.END, "")

			listbox.insert(tk.END, "------END of Course Names match -----")
			listbox.insert(tk.END, "")

		if counter == 0:
			listbox.insert(tk.END, "No matches")
	
	conn.commit()
	conn.close()
	search_student.delete(0,END)

def delete_student():
	test = select_student.get()
	if test.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT * FROM students WHERE id_number= " + select_student.get())
	records = c.fetchall()

	if records:
		c.execute("DELETE from students WHERE id_number= " + select_student.get())

		select_student.delete(0,END)

	else:
		messagebox.showerror("ID Number Error", "The ID Number does not exist. \n Please input the correct ID number of the student you want to delete.")
		return
	conn.commit()
	conn.close()

def edit_student():
	test = select_student.get()
	if test.strip() == "":
		messagebox.showerror("Input Error", "You cannot Input a blank!")
		return

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	c.execute("SELECT * FROM students WHERE id_number= " + select_student.get())
	records = c.fetchall()

	if records:
		# Disable Edit of ID number
		id_num.grid_forget()
	 
		c.execute("SELECT * FROM students WHERE id_number= " + select_student.get())
		records = c.fetchall()

		for record in records:
			f_name.insert(0, record[0])
			m_name.insert(0, record[1])
			l_name.insert(0, record[2])
			id_num.insert(0, record[3])
			gender.set(value=record[4])
			yearlvl.set(value=record[5])
			course.insert(0, record[6])

		# Submit Button
		submit_btn = Button(root, text="CONFIRM EDIT", command=check_course_code_exists,
			font=('Arial', 10, 'bold'), fg='white', bg='#35d17c')
		submit_btn.grid(row=8, column=1, columnspan=2, pady=10, padx=(0,14), ipadx=38)

		c.execute("DELETE from students WHERE id_number= " + select_student.get())
		select_student.delete(0,END)

	else:
		messagebox.showerror("ID Number Error", "The ID Number does not exist. \n Please input the correct ID number of the student you want to edit.")
		return	

	conn.commit()
	conn.close()

def list_down_students():
	students_list = Tk()
	students_list.title('LIST OF STUDENTS')
	students_list.geometry("500x500")
	students_list.resizable(width=False, height=False)
	students_list.configure(bg='#252525')

	formats=choice.get()

	listbox = tk.Listbox(students_list, width=70)
	listbox.config(font=('Arial', 10, 'bold'),bg='#252525', fg='#35d17c')
	listbox.pack(side=tk.LEFT, fill=tk.BOTH)

	scrollbar = tk.Scrollbar(students_list)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

	listbox.config(yscrollcommand=scrollbar.set)
	scrollbar.config(command=listbox.yview)

	conn = sqlite3.connect('SSIS_Pineda.db')
	c = conn.cursor()

	if formats == "SORTED BY NAME":
		c.execute("SELECT * FROM students ORDER BY last_name")
		records = c.fetchall()

		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			s_course_code = record[6]
			listbox.insert(tk.END, str(record[2]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n")

	elif formats == "SORTED BY ID NUMBER":
		c.execute("SELECT * FROM students ORDER BY id_number")
		records = c.fetchall()

		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			s_course_code = record[6]
			listbox.insert(tk.END, str(record[3]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[4]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n")

		
	elif formats == "SORTED BY GENDER":
		c.execute("SELECT * FROM students ORDER BY gender")
		records = c.fetchall()

		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			s_course_code = record[6]
			listbox.insert(tk.END, str(record[4]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n")

	elif formats == "SORTED BY YEAR LEVEL":
		c.execute("SELECT * FROM students ORDER BY year_level")
		records = c.fetchall()

		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			s_course_code = record[6]
			listbox.insert(tk.END, str(record[5]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[6]) + "\n")

	elif formats == "SORTED BY COURSE":
		c.execute("SELECT * FROM students ORDER BY s_course_code")
		records = c.fetchall()

		for record in records:
			first_name = record[0]
			middle_name = record[1]
			last_name = record[2] 
			id_number = record[3] 
			gender = record[4]
			year_level = record[5]
			s_course_code = record[6]
			listbox.insert(tk.END, str(record[6]) + " | " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + "\n")

	else:
		c.execute("SELECT *, oid FROM students")
		records = c.fetchall()
		print(records)

		for record in records:
			listbox.insert(tk.END, str(record[7]) + " - " + str(record[0]) + " | " + str(record[1]) + " | " + str(record[2]) + " | " + str(record[3]) + " | " + str(record[4]) + " | " + str(record[5]) + " | " + str(record[6]) + "\n")

	conn.commit()
	conn.close()

def submit(): # add error message if duplicate ID number
	global gender
	global yearlvl
	global course

	# Submit Button
	submit_btn = Button(root, text="ADD STUDENT", command=submit,
		font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c')
	submit_btn.grid(row=8, column=1, columnspan=2, pady=10, padx=(0,14), ipadx=40)

	id_num.grid(row=4, column=1, padx=20)

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
	course.delete(0,END)

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

course = Entry(root, width=30, fg='white', bg='#252525')
course.grid(row=7, column=1)

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
choices_listed.config(width=20, bg='#35d17c', font=('Arial', 9, 'bold'))
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

course_list_label = Label(root, text="COURSE CODE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
course_list_label.grid(row=7,column=0)

student_list_down_label = Label(root, text="STUDENT LIST", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
student_list_down_label.grid(row=9,column=0)

select_student_label = Label(root, text="INPUT ID NUMBER", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
select_student_label.grid(row=11,column=0)

search_student_label = Label(root, text="SEARCH", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
search_student_label.grid(row=14,column=0)

add_course_name_label = Label(root, text="COURSE NAME", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
add_course_name_label.grid(row=16,column=0)

add_course_code_label = Label(root, text="COURSE CODE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
add_course_code_label.grid(row=17,column=0)

select_course_key_label = Label(root, text="INPUT COURSE CODE", 
	font=('Arial', 10, 'bold'), fg='#35d17c', bg='#252525')
select_course_key_label.grid(row=19,column=0, pady=(2,0))

# Submit Button
submit_btn = Button(root, text="ADD STUDENT", command=check_course_code_exists,
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

# Search student Button
search_btn = Button(root, text="SEARCH",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=student_search)
search_btn.grid(row=15, column=1, ipadx=60)

# Add Course Button
add_course_btn = Button(root, text="ADD COURSE",
	font=('Arial', 10, 'bold'), fg='#252525', bg='#35d17c', command=check_course_code_duplicate)
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

conn.commit()
conn.close()
root.mainloop()