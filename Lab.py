from tkinter import *
from tkinter import font,filedialog
import json
from abc import ABC, abstractmethod

class Person:

    __next_id = 0
    
    def __init__(self, first_name, surname, last_name) -> None:
        self.first_name = first_name
        self.surname = surname
        self.last_name = last_name
        self.id = self.get_id()

    @classmethod
    def get_id(cls):
        cls.__next_id+=1
        return cls.__next_id-1
    
    def __repr__(self) -> str:
        
        return f"{self.first_name} {self.surname} {self.last_name}"
        
class Student(Person):
    
    def __init__(self, first_name, surname, last_name, course) -> None:
        super().__init__(first_name, surname, last_name)
        self.course = course

class Teacher(Person):
    
    def __init__(self, first_name, surname, last_name, group) -> None:
        super().__init__(first_name, surname, last_name)
        self.group = group

class Institution(ABC):

    @abstractmethod
    def get_students(self):
        pass
    
    @abstractmethod
    def get_teachers(self):
        pass

    def sort_per_alph(self, persons):
        return sorted(persons, key=lambda person: person.last_name+person.first_name+person.last_name)
    
    def sort_teach_alph(self):
        return self.sort_per_alph(self.get_teachers())

    def sort_stud_alph(self):
        return self.sort_per_alph(self.get_students())

    def sort_stud_course(self):
        return sorted(self.get_students(), key=lambda student: student.course)
    
    def get_students_course(self, course):
        return list(filter(lambda student: student.course==course, self.get_students()))

    def sort_stud_by_alph_with_course(self, course):
        return self.sort_per_alph(self.get_students_course(course))
    
class Department(Institution):

    def __init__(self, name, students=set(),teachers=set()) -> None:
        self.name = name
        self.students = students
        self.teachers = teachers
    
    def __repr__(self) -> str:
        
        return f"{self.name}, Students: {self.students}, Teachers: {self.teachers}"
    
    def get_students(self):
        return self.students

    def get_teachers(self):
        return self.teachers
    
class Faculty(Institution):
    
    def __init__(self, name, departments=set()) -> None:
        self.name = name
        self.departments = departments
    
    def __repr__(self) -> str:
        
        return f"{self.name}, Departments: {self.departments}"
    
    def get_students(self):
        students = set()
        for department in self.departments:
            for student in department.students:
                students.add(student)
        return students

    def get_teachers(self):
        teachers = set()
        for department in self.departments:
            for teacher in department.teachers:
                teachers.add(teacher)
        return teachers

class University(Institution):

    def __init__(self, name, faculties=set()) -> None:
        self.name = name
        self.faculties = faculties

    def __repr__(self) -> str:
        
        return f"{self.name}, Faculties: {self.faculties}"
    
    def get_students(self):
        students = set()
        for faculty in self.faculties:
            for department in faculty.departments:
                for student in department.students:
                    students.add(student)
        return students

    def get_teachers(self):
        teachers = set()
        for faculty in self.faculties:
            for department in faculty.departments:
                for teacher in department.teachers:
                    teachers.add(teacher)
        return teachers


def main():
    UI()
    
def UI():
    window = Tk()
    window.title('University')
    
    window.option_add("*Font", font.Font(size=14))

    university = University("NaUKMA")
    selected = university
    

    def choose_file():
        file_path = filedialog.askopenfilename(filetypes = (
            ('JSON', '*.json'),
            ('All files', '*.*')
        ))
        with open(file_path, "r",encoding='utf-8') as f:
            data = json.load(f)
            f.close
            return set_university_with_json(data)
        
    def set_university_with_json(json):
        nonlocal university
        nonlocal window
        university.faculties = {
                Faculty(name=faculty["name"],
                    departments={Department(department["name"], 
                                    students={Student(
                                        student["first_name"], 
                                        student["surname"], 
                                        student["last_name"],
                                        student["course"]) for student in department["students"]
                                    },
                                    teachers = {Teacher(
                                        teacher["first_name"], 
                                        teacher["surname"], 
                                        teacher["last_name"],
                                        teacher["group"]) for teacher in department["teachers"]
                                    }
                                        ) for department in faculty["departments"]
                    }) for faculty in json["faculties"]}
        update_fac()
        update_interface()

        

    #-------------------------------------------------------------------
    selection_frame = Frame(window)
    selection_frame.grid(row=0,column=0)

    #-------------------------------------------------------------------

    def choose_faculty():
        nonlocal selected
        selected = university

        #print(selected)

        return [faculty.name for faculty in university.faculties]

    def choose_department():
        choose_faculty()
        if faculty_string.get()!=faculty_default_string:
            nonlocal selected
            selected = list(filter(lambda faculty: faculty.name == faculty_string.get(), university.faculties))[0]

            #print(selected)

            return [department.name for department in selected.departments]
        else:
            return []
    
    def choose_person():
        choose_department()
        if department_string.get()!=department_default_string:
            nonlocal selected
            selected = list(filter(lambda department: department.name == department_string.get(), selected.departments))[0]

            #print(selected)

            return [f"{person.last_name} {person.first_name} {person.surname}" for person in selected.students.union(selected.teachers)]
        else:
            return []
    
    
    

    #-------------------------------------------------------------------
    file_button = Button(window, text="Choose file", command=choose_file)
    file_button.grid(row=5,column=0, sticky=E+W)
    #-------------------------------------------------------------------

    
    
    faculty_default_string = "Faculty"
    department_default_string = "Department"
    person_default_string = "Person"

    faculty_string = StringVar(value=faculty_default_string)
    department_string = StringVar(value=department_default_string)
    person_string = StringVar(value=person_default_string)

    

    faculty_drop = OptionMenu( selection_frame , faculty_string,  faculty_default_string, *[])
    faculty_drop.grid(row=0,column=0)
    
    department_drop = OptionMenu( selection_frame , department_string, department_default_string, *[])
    department_drop.grid(row=0,column=1)
    
    person_drop = OptionMenu( selection_frame , person_string, person_default_string, *[])
    person_drop.grid(row=0,column=2)
    
    def get_selected_faculty():
        return list(filter(lambda faculty: faculty.name == faculty_string.get(), university.faculties))[0]

    def get_selected_department():
        return list(filter(lambda department: department.name == department_string.get(), get_selected_faculty().departments))[0]

    def delete():
        if isinstance(selected, Person):
            department = get_selected_department()

            if selected in department.teachers:
                department.teachers.remove(selected)
            else:
                
                department.students.remove(selected)

        if isinstance(selected, Department):
            faculty = get_selected_faculty()
            faculty.departments.remove(selected)

        if isinstance(selected, Faculty):
            university.faculties.remove(selected)

        update()

    def create():
        if isinstance(selected, Person):
            
            if person_cg_entry.get().isdigit():
                if person_str.get() == "Student":
                    get_selected_department().students.add(Student(
                        person_first_name_entry.get(),
                        person_surname_entry.get(),
                        person_last_name_entry.get(),
                        int(person_cg_entry.get())
                    ))
                if person_str.get() == "Teacher":
                    get_selected_department().teachers.add(Teacher(
                        person_first_name_entry.get(),
                        person_surname_entry.get(),
                        person_last_name_entry.get(),
                        int(person_cg_entry.get())
                    ))

        elif isinstance(selected, Faculty):
            selected.departments.add(Department(institution_name_entry.get()))
        else:
            selected.faculties.add(Faculty(institution_name_entry.get()))
        
        update()

    def edit():
        if isinstance(selected, Person):
            
            if person_cg_entry.get().isdigit() or (not person_cg_entry.get()):
                selected.first_name = person_first_name_entry.get() if person_first_name_entry.get() else selected.first_name
                selected.surname = person_surname_entry.get() if person_surname_entry.get() else selected.surname
                selected.last_name = person_last_name_entry.get() if person_last_name_entry.get() else selected.last_name

                if isinstance(selected, Student):
                    selected.course = int(person_cg_entry.get()) if person_cg_entry.get() else selected.course
                if isinstance(selected, Teacher):
                    selected.group = int(person_cg_entry.get()) if person_cg_entry.get() else selected.group

        elif isinstance(selected, Institution):
            selected.name = institution_name_entry.get() if institution_name_entry.get() else selected.name
        
        update()
    
    def find():
        if find_by.get() == "Student":
            for student in (filter(lambda student: \
                            (student.first_name == find_first_name_entry.get() or not find_first_name_entry.get()) and\
                            (student.surname == find_surname_entry.get() or not find_surname_entry.get()) and\
                            (student.last_name == find_last_name_entry.get() or not find_last_name_entry.get()) and\
                            (str(student.first_name) == find_first_name_entry.get() or not find_first_name_entry.get()), selected.get_students())):
                print(student)
        else:
            for teacher in (filter(lambda teacher: \
                            (teacher.first_name == find_first_name_entry.get() or not find_first_name_entry.get()) and\
                            (teacher.surname == find_surname_entry.get() or not find_surname_entry.get()) and\
                            (teacher.last_name == find_last_name_entry.get() or not find_last_name_entry.get()) and\
                            (str(teacher.first_name) == find_first_name_entry.get() or not find_first_name_entry.get()), selected.get_teachers())):
                print(teacher)

    def sort_stud():
        for student in selected.sort_stud_alph():
            print(student)

    def sort_teach():
        for student in selected.sort_teach_alph():
            print(student)

    def cour_stud_f():
        for student in selected.get_students_course(int(cour_entry.get())):
            print(student)

    def cour_sort_stud():
        for student in selected.sort_stud_by_alph_with_course(int(cour_entry.get())):
            print(student)
    
    
    
    

    #----------------ALL---------------------#

    changing_frame = Frame(window)
    changing_frame.grid(row=1,column=0)

    delete_butt = Button(changing_frame, text="Delete", command=delete, bg="#f00")
    delete_butt.grid(row=0, column=0)

    edit_butt = Button(changing_frame, text="Edit", command=edit, bg="#00f")
    edit_butt.grid(row=0, column=1)

    create_butt = Button(changing_frame, text="Create", command=create, bg="#0f0")
    create_butt.grid(row=0, column=2)

    changing_frame.grid(row=1, column=0)

    #----------------INSTITUTION---------------------#

    institution_name_frame = Frame(window)

    institution_name_label = Label(institution_name_frame, text="Name")
    institution_name_label.grid(row=0, column=0)
    institution_name_entry = Entry(institution_name_frame)
    institution_name_entry.grid(row=0, column=1)

    #institution_name_frame.grid(row=2, column=0)



    #----------------PERSON---------------------#

    person_name_frame = Frame(window)

    person_str = StringVar(person_name_frame, "Student")
    person_om = OptionMenu(person_name_frame, person_str, *["Student", "Teacher"])
    person_om.grid(row=0, column=0)

    person_last_name_label = Label(person_name_frame, text="Прізвище")
    person_last_name_label.grid(row=1, column=0)

    person_last_name_entry = Entry(person_name_frame)
    person_last_name_entry.grid(row=1, column=1)
  

    person_first_name_label = Label(person_name_frame, text="Ім'я")
    person_first_name_label.grid(row=2, column=0)

    person_first_name_entry = Entry(person_name_frame)
    person_first_name_entry.grid(row=2, column=1)
    

    person_surname_label = Label(person_name_frame, text="По-батькові")
    person_surname_label.grid(row=3, column=0)

    person_surname_entry = Entry(person_name_frame)
    person_surname_entry.grid(row=3, column=1)

    person_cg_label = Label(person_name_frame, text="Course/group")
    person_cg_label.grid(row=4, column=0)

    person_cg_entry = Entry(person_name_frame)
    person_cg_entry.grid(row=4, column=1)
    
    #person_name_frame.grid(row=2, column=0)



    #----------------INSTITUTION---------------------#

    find_person_frame = Frame(window)

    find_by = StringVar(find_person_frame, "Student")
    find_by_om = OptionMenu(find_person_frame, find_by, *["Student", "Teacher"])
    find_by_om.grid(row=0, column=0)

    find_last_name_label = Label(find_person_frame, text="Прізвище")
    find_last_name_label.grid(row=1, column=0)

    find_last_name_entry = Entry(find_person_frame)
    find_last_name_entry.grid(row=1, column=1)
  

    find_first_name_label = Label(find_person_frame, text="Ім'я")
    find_first_name_label.grid(row=2, column=0)

    find_first_name_entry = Entry(find_person_frame)
    find_first_name_entry.grid(row=2, column=1)
    

    find_surname_label = Label(find_person_frame, text="По-батькові")
    find_surname_label.grid(row=3, column=0)

    find_surname_entry = Entry(find_person_frame)
    find_surname_entry.grid(row=3, column=1)

    find_course_label = Label(find_person_frame, text="Course")
    find_course_label.grid(row=4, column=0)

    find_cg_entry = Entry(find_person_frame)
    find_cg_entry.grid(row=4, column=1)

    find_get_butt = Button(find_person_frame, text="Get", command=find)
    find_get_butt.grid(row=5, column=0)



    #----------------INSTITUTION---------------------#

    return_frame = Frame(window)

    sort_label = Label(return_frame, text="Sort: ")
    sort_label.grid(row=0, column=0)

    sort_stud_butt = Button(return_frame, text="students", command=sort_stud)
    sort_stud_butt.grid(row=0, column=1)

    sort_teach_butt = Button(return_frame, text="teachers", command=sort_teach)
    sort_teach_butt.grid(row=0, column=2)



    cour_label = Label(return_frame, text="get students on: ")
    cour_label.grid(row=1, column=0)

    cour_stud = Button(return_frame, text="course", command=cour_stud_f)
    cour_stud.grid(row=1, column=1)

    cour_stud_sort = Button(return_frame, text="course sorted", command=cour_sort_stud)
    cour_stud_sort.grid(row=1, column=2)

    cour_label = Label(return_frame, text="Course: ")
    cour_label.grid(row=3, column=0)

    cour_entry = Entry(return_frame)
    cour_entry.grid(row=3, column=1)

    #return_frame.grid(row=4, column=0)





    def update_interface():

        if isinstance(selected, Person):
            institution_name_frame.grid_forget()
            return_frame.grid_forget()
            find_person_frame.grid_forget()

            person_name_frame.grid(row=2, column=0)
            
        if isinstance(selected, Institution):
            institution_name_frame.grid(row=2, column=0)
            return_frame.grid(row=4, column=0)
            find_person_frame.grid(row=3, column=0)

            person_name_frame.grid_forget()


    faculty_string.trace_id = faculty_string.trace("w", lambda name, index, mode, sv=faculty_string: update_dep(dep_string = department_default_string) or update_interface())
    department_string.trace_id = department_string.trace("w", lambda name, index, mode, sv=department_string: update_per(per_string = person_default_string) or update_interface())
    person_string.trace_id = person_string.trace("w", lambda name, index, mode, sv=person_string: update_last() or update_interface())

    def update():
        update_fac(faculty_default_string)

    def update_fac(fac_string = None):
        nonlocal faculty_string
        nonlocal faculty_drop

        if fac_string:
            faculty_string.set(fac_string)
        
        menu = faculty_drop["menu"]
        menu.delete(0, "end")
        for string in [faculty_default_string] + choose_faculty():
            menu.add_command(label=string,
                             command=lambda value=string: faculty_string.set(value))
        
    
    def update_dep(dep_string = None):
        choose_faculty()
        nonlocal department_string
        nonlocal department_drop

        if dep_string:
            department_string.set(dep_string)

        menu = department_drop["menu"]
        menu.delete(0, "end")
        for string in [department_default_string] + choose_department():
            menu.add_command(label=string,
                             command=lambda value=string: department_string.set(value))

        
    def update_per(per_string = None):
        nonlocal person_string
        nonlocal person_drop

        if per_string:
            person_string.set(per_string)

        menu = person_drop["menu"]
        menu.delete(0, "end")
        for string in [person_default_string] + choose_person():
            menu.add_command(label=string,
                             command=lambda value=string: person_string.set(value))

        
    def update_last():
        choose_person()
        if person_string.get()!=person_default_string:
            nonlocal selected
            selected = list(filter(lambda person: f"{person.last_name} {person.first_name} {person.surname}" == person_string.get(), selected.students.union(selected.teachers)))[0]
            #(selected)

    update_fac()
    update_interface()
    

    

    

    window.mainloop()

if __name__ == "__main__":
    main()