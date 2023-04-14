from tkinter import *
from tkinter import font,filedialog
import json

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

class Department:

    def __init__(self, name, students=set(),teachers=set()) -> None:
        self.name = name
        self.students = students
        self.teachers = teachers
    
    def __repr__(self) -> str:
        
        return f"{self.name}, Students: {self.students}, Teachers: {self.teachers}"
    
class Faculty:
    
    def __init__(self, name, departments=set()) -> None:
        self.name = name
        self.departments = departments
    
    def __repr__(self) -> str:
        
        return f"{self.name}, Departments: {self.departments}"

class University:

    def __init__(self, name, faculties=set()) -> None:
        self.name = name
        self.faculties = faculties

    def __repr__(self) -> str:
        
        return f"{self.name}, Faculties: {self.faculties}"


def main():
    UI()
    
def UI():
    window = Tk()
    window.title('University')
    
    window.option_add("*Font", font.Font(size=14))

    university = University("NaUKMA")
    selected = None

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
        update()

        

    #-------------------------------------------------------------------
    frame = Frame(window)
    frame.grid(row=0,column=0)

    #-------------------------------------------------------------------

    def choose_faculty():
        
        return [faculty.name for faculty in university.faculties]

    def choose_department():
        if faculty_string.get()!=faculty_default_string:
            nonlocal selected
            selected = list(filter(lambda faculty: faculty.name == faculty_string.get(), university.faculties))[0]
            return [department.name for department in selected.departments]
        else:
            return []
    
    def choose_person():
        if department_string.get()!=department_default_string:
            nonlocal selected
            selected = list(filter(lambda department: department.name == department_string.get(), selected.departments))[0]
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

    def update():
        print("updating")
        faculty_drop = OptionMenu( frame , faculty_string,  faculty_default_string, *choose_faculty())
        faculty_drop.grid(row=0,column=0)
        faculty_string.trace("w", lambda name, index, mode, sv=faculty_string: update())

        department_drop = OptionMenu( frame , department_string, department_default_string, *choose_department())
        department_drop.grid(row=0,column=1)
        department_string.trace("w", lambda name, index, mode, sv=department_string: update())

        person_drop = OptionMenu( frame , person_string, person_default_string, *choose_person())
        person_drop.grid(row=0,column=2)
        person_string.trace("w", lambda name, index, mode, sv=department_string: update())

        if person_string.get()!=person_default_string:
            nonlocal selected
            selected = list(filter(lambda person: f"{person.last_name} {person.first_name} {person.surname}" == person_string.get(), selected.students.union(selected.teachers)))[0]

    update()

    window.mainloop()

if __name__ == "__main__":
    main()