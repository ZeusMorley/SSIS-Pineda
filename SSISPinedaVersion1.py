#SSIS version 1 by Zeus Morley S. Pineda
import operator
import csv
students_list = []
course_list = ["NULL"]
course_list_holder = []
sorting_list = []
output_list_students = []
output_list_courses = []

class Student: #Student object
    def __init__(self, name, ID, course, courseid):
        self.name = name
        self.ID = ID
        self.course = course
        self.courseid = courseid

    def __repr__(self):
        return str(self.name) + ' | ' + str(self.ID) + ' | ' + str(course_list[self.courseid])

def choice_of_action():
    while True:
        choice_action = str(input("What would you like to do?\n1-Add Student.\n2-Add Course\n3-Delete Course.\n4-Delete student.\n5-Edit a student.\n6-Edit a course.\n7-Search a student.\n8-Search a course\n9-List of students.\n10-List of Courses.\n:"))
        if choice_action == '1':  # Add student
            Add_student()
            break
        if choice_action == '2':  # Add Course
            Add_course()
            break
        if choice_action == '3':  # Delete Course
            Delete_course()
            break
        if choice_action == '4':  # Delete Student
            Delete_student()
            break
        if choice_action == '5':  # Edit a student
            Edit_student()
            break
        if choice_action == '6':  # Edit a course
            Edit_course()
            break
        if choice_action == '7':  # Search a student
            Search_student()
            break
        if choice_action == '8':  # Search a Course
            Search_course()
            break
        if choice_action == '9':  # List of Students
            List_student()
            break
        if choice_action == '10': # List of Courses
            List_courses()
            break
        else:
            print("Please choose a number in the choices(1 to 10)")

def List_courses():
    print("\nList of Courses:")
    for i in range(len(course_list)-1):
        i1 = i+1
        print(str(i1) + "-" + course_list[i1])

def List_students(version):
    print("List of Students:( Name | ID-Number | Course ):")
    if version == 1:
        i2 = 0
        for i in students_list:
            i2 = i2 + 1
            print(str(i2) + "- " + i.name + " | " + str(i.ID) + " | " + course_list[i.courseid])
    else:
        for i in students_list:
            print(i.name + " | " + str(i.ID) + " | " + course_list[i.courseid])
#Zeus
def Add_student(): #add filters for choosing course
    if len(course_list) < 2:
        print("You need an available course to add a student.")
        Want_Add_Course()
    else:
        print("You will give the name, ID number, and course of the student.")
        Name = str(input("Input the name in (Surname Firstname Middlename) format:"))
        ID_number = str(input("Input the ID number in (yyyy abcd) format:"))

        while True:
            List_courses()
            courseid = int(input("Choose among the courses:"))
            course = str(course_list[int(courseid)])
            if courseid <= len(course_list) and courseid > 0:
                student = Student(Name.upper(), ID_number, course.upper(), courseid)
                students_list.append(student)
                print("Student " + Name.upper() + " with ID number " + ID_number + " of " + course.upper() + " has been successfully added.")
                break
            else:
                print("Please choose a course number among the choices (1 to " + str(len(course_list)) + ")")

def Add_course():
    new_course = input("Give the name of the new course: ")
    course_list.append(new_course)
    print("The course " + new_course + " has been successfully added.\n")
    List_courses()

def Delete_course(): #delete students under deleted course
    if len(course_list) > 1:
        confirm = str(input("Deleting a course will unenroll all students under it, are you sure?\n1-yes\n2-no\n:"))
        if confirm == '1':
            List_courses()
            while True:
                chosen = int(input("\nChoose a course to delete:"))
                if 0 < chosen <= len(course_list):
                    i2 = chosen
                    for i in students_list:
                        if course_list[i.courseid] == course_list[i2]:
                            i.courseid = 0

                    print("Course " + str(course_list[i2]) + " has been successfully removed.")
                    course_list.pop(i2)
                    List_courses()
                    ver = 0
                    List_students(ver)
                    break
                else:
                    print("Please choose among the choices only\n")
                    List_courses()
        elif confirm == '2':
            return
        else:
            print("Please choose a number in the choices (1 or 2)\n")
    else:
        Want_Add_Course()
def Want_Add_Course():
    print("There are no courses available for now, please add one first.\n")
    while True:
        addcoursenow = int(input("Do you want to add a course?\n1-Yes\n2-No\n:"))
        if addcoursenow == 1:
            Add_course()
            break
        if addcoursenow == 2:
            break

        else:
            print("Please choose a number in the choices (1 or 2)\n")

def sorted_list(bywhat):
    if bywhat == '1':
        print("List of names in alphabetical order: ")
        sorting_list = sorted(students_list, key=operator.attrgetter('name', 'ID', 'course'))
        for i in sorting_list:
            print(i)

    elif bywhat == '2':
        print("List of ID numbers in ascending order: ")
        sorting_list = sorted(students_list, key=operator.attrgetter('ID', 'name', 'course'))
        for i in sorting_list:
            print(i)

    elif bywhat == '3':
        print("List of courses in alphabetical order: ")
        sorting_list = sorted(students_list, key=operator.attrgetter('course', 'name', 'ID'))
        for i in sorting_list:
            print(i)

def rev_sorted_list(bywhat):
    if bywhat == '1':
        print("List of names in reverse alphabetical order: ")
        sorting_list = sorted(students_list, reverse=True, key=operator.attrgetter('name', 'ID', 'course'))
        for i in sorting_list:
            print(i)

    elif bywhat == '2':
        print("List of ID numbers in descending order: ")
        sorting_list = sorted(students_list, reverse=True, key=operator.attrgetter('ID', 'name', 'course'))
        for i in sorting_list:
            print(i)

    elif bywhat == '3':
        print("List of courses in reverse alphabetical order: ")
        sorting_list = sorted(students_list, reverse=True, key=operator.attrgetter('course', 'name', 'ID'))
        for i in sorting_list:
            print(i)
#Zeus
def Delete_student():
    grab_name = " "
    if len(students_list) > 0:
        ver = 1
        List_students(ver)
        while True:
            chosen = int(input("\nChoose a student to delete:"))
            if(chosen<=len(students_list)):
                ver = 0
                i3 = 0
                i = chosen
                for i2 in students_list:
                    if i3 == i:
                        grab_name = i2.name
                        break
                    i3 += 1
                print("Student " + str(grab_name) + " has been successfully removed.\n")
                del students_list[i-1]
                List_students(ver)
                break
            else:
                ver=0
                print("Please choose among the choices(1 to " + str(len(students_list)) + ")\n")
                List_students(ver)
    else:
        print("There are no students available to delete.")

def Edit_student():
    ver=1
    i3=0
    List_students(ver)
    chosen = int(input("\nChoose a student to edit:"))
    i = chosen - 1
    for i2 in students_list:
        if i3 == i:
            grab_name = str(i2.name)
            grab_ID_number = str(i2.ID)
            grab_course = str(course_list[i2.courseid])
            grab_courseid = int(i2.courseid+1)
        i3 += 1
    print("You have chosen " + grab_name + ", " + grab_ID_number + " of " + grab_course + ".")

    while True:
        choice = str(input("What do you wish to edit?\n1-Name\n2-ID number\n3-course\n:"))
        if choice == '1':
            Name = input("Please enter the new name of (" + grab_name + "): ")
            ID_number = str(grab_ID_number)
            course = str(grab_course)
            courseid = int(grab_courseid)

            del students_list[i]
            student = Student(Name.upper(), ID_number, course.upper(), courseid)
            students_list.append(student)

            print("Successfully changed the name of: " + grab_name + " into " + Name.upper() + ".")
            break

        elif choice == '2':
            Name = str(grab_name)
            ID_number = input("Please enter the new ID number of (" + grab_name + "):")
            course = str(grab_course)
            courseid = int(grab_courseid)

            del students_list[i]
            student = Student(Name.upper(), ID_number, course.upper(), courseid)
            students_list.append(student)

            print("Successfully changed the ID number of: " + grab_name + " from " + grab_ID_number + " to " + ID_number + ".")
            break

        elif choice == '3':
            Name = str(grab_name)
            ID_number = str(grab_ID_number)
            List_courses()
            courseid = int(input("Please enter the new course of (" + grab_name + "): "))
            course = str(course_list[int(courseid)])

            del students_list[i]
            student = Student(Name.upper(), ID_number, course.upper(), courseid)
            students_list.append(student)

            print("Successfully changed the course of: " + grab_name + " from " + grab_course + " to " + course + ".")
            break

        else:
            print("Please choose among the choices. (1, 2, or 3)")


def Search_student():
    search = str(input("Who are you looking for? You can input the full name or ID_number\n:"))
    for i in students_list:
        if i.name == search.upper():
            print("We found: " + i.name + " | " + i.ID)
            return
        elif i.ID == search.upper():
            print("We found: " + i.name + " | " + i.ID)
            return
    print("Sorry the student is not in the system.")
#Zeus
def Search_course():
    counter = 0
    search = str(input("What course are you looking for? Please input the course name\n:"))
    print("Courses similar to your search:\n")
    for i in course_list:
        if i == search:
            print(i)
            counter = counter + 1
        elif i == search.upper():
            print(i)
            counter = counter + 1
        elif i == search.lower():
            print(i)
            counter = counter +1
    if counter == 0:
        print("Sorry the course is not in the system.")
    else:
        print("\nFound: (" + str(counter) + ") courses.")

def List_student():
    while True:
        SortedOrNot = str(input("\nDo you want the List sorted or not?\n1-Yes\n2-No\n:"))
        if SortedOrNot == '1':
            while True:
                ByWhat = str(input("\nHow do you want it to be sorted? By: \n1-Name\n2-ID-number\n3-course\n:"))
                if ByWhat == '1' or ByWhat == '2' or ByWhat == '3':
                    while True:
                        AscOrDes = str(input("Do you want it... \n1-ascending\n2-descending\n:"))
                        if AscOrDes == '1':
                            sorted_list(ByWhat)
                            break
                        elif AscOrDes == '2':
                            rev_sorted_list(ByWhat)
                            break
                        else:
                            print("\nPlease choose a number among the choices(1 or 2)")
                    break
                else:
                    print("\nPlease choose a number among the choices(1, 2 or 3)")
            break
        elif SortedOrNot == '2':
            ver = 0
            List_students(ver)
            break
        else:
            print("Please choose a number among the choices(1 or 2)")

def Edit_course():
    global course_list
    i3=0
    i4=0
    course_holder = " "
    List_courses()
    chosen = int(input("\nChoose a Course to edit\n:"))
    i = chosen
    for i2 in course_list:
        if i3 == i:
            grab_course = str(i2)
        i3 += 1
    print("You have chosen " + grab_course + ".")

    course = input("Please enter the new name of Course: " + grab_course + "\n: ")

    for courses in course_list:
        if i4 == i:
            course_list_holder.append(course)
        else:
            course_holder = courses
            course_list_holder.append(course_holder)
        i4 = i4 + 1

    course_list = course_list_holder.copy()
    course_list_holder.clear()

    print("\nSuccessfully changed the name of the Course: " + grab_course + " into " + course + ".")

# Start Of Main Function
print("Simple Student Information System\n")  # Greetings

choice_of_action()  # Choice Function

# Another Action
while True:
    choice_repeat = str(input("\nWould you like to do another action?\n1-Yes\n2-No\n:"))
    if choice_repeat == '1':
        choice_of_action()
    elif choice_repeat =='2':
        break
    else:
        print("Please choose a number in the choices(1 or 2)")

for i in students_list:
    compiled_students = str(i.name + " | " + str(i.ID) + " | " + course_list[i.courseid])
    output_list_students.append(compiled_students)

file_path_students = r'C:\SSISProjectsPineda\SSISPinedaOutputStudents.csv'
with open(file_path_students, 'w', newline='') as csvfile:
    for i in output_list_students:
        csv_line_students = ' '.join(str(element) for element in i)
        csvfile.write(csv_line_students + '\n')


for i in course_list:
    output_list_courses.append(i)

file_path_courses = r'C:\SSISProjectsPineda\SSISPinedaOutputCourses.csv'
with open(file_path_courses, 'w', newline='') as csvfile:
    for i in output_list_courses:
        csv_line_courses = ' '.join(str(element) for element in i)
        csvfile.write(csv_line_courses + '\n')