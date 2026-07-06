"""
SNo. 220526: BACKEND CONTROLLER - MAIN APP
"""
# Import 
from waitlist_queue import WaitlistQueue
from course_list import CourseList
from std_hashmap import StudentHashmap
from algorithms import dfs_check_prerequisites, binary_search_course, merge_sort_students


class RegistrationController:
    def __init__(self):
        self.students = StudentHashmap()
        self.courses = CourseList()
        self.waitlists = {}
        self._load_dummy_data()
        print("✅ System Ready!")
    
    def _load_dummy_data(self):
        students = {
            'S001': {'name': 'John Doe', 'year': 4, 'gpa': 3.8, 'completed': ['CS101']},
            'S002': {'name': 'Jane Smith', 'year': 3, 'gpa': 3.5, 'completed': []},
            'S003': {'name': 'Alice Johnson', 'year': 2, 'gpa': 3.2, 'completed': []},
            'S004': {'name': 'Bob Williams', 'year': 4, 'gpa': 2.9, 'completed': ['CS101', 'CS201']},
        }
        for sid, data in students.items():
            self.students.insert(sid, data)
        
        courses = [
            {'code': 'CS101', 'name': 'Intro Programming', 'capacity': 2},
            {'code': 'CS201', 'name': 'Data Structures', 'capacity': 2},
            {'code': 'CS301', 'name': 'Algorithms', 'capacity': 1},
        ]
        for course in courses:
            self.courses.add_course(course)
        
        self.courses.add_prerequisite('CS201', 'CS101')
        self.courses.add_prerequisite('CS301', 'CS201')
        
        for course in self.courses.get_all_courses():
            self.waitlists[course['code']] = WaitlistQueue()
    
    # MAIN FUNCTIONS 
    
    def register_student(self, student_id, course_code):
        if not self.students.get(student_id):
            return "Student not found"
        if not self.courses.get_course(course_code):
            return "Course not found"
        
        student = self.students.get(student_id)
        if not dfs_check_prerequisites(course_code, student.get('completed', []), self.courses):
            return "Missing prerequisites"
        
        course = self.courses.get_course(course_code)
        if len(self.courses.get_enrolled(course_code)) < course['capacity']:
            self.courses.enroll_student(course_code, student_id)
            return "Registered!"
        else:
            self.waitlists[course_code].enqueue(student_id)
            return "Added to waitlist"
    
    def search_course(self, course_code):
        courses = self.courses.get_all_courses()
        courses.sort(key=lambda x: x['code'])
        return binary_search_course(courses, course_code)
    
    def drop_course(self, student_id, course_code):
        if not self.courses.get_course(course_code):
            return "Course not found"
        self.courses.drop_student(course_code, student_id)
        if not self.waitlists[course_code].is_empty():
            next_student = self.waitlists[course_code].dequeue()
            self.courses.enroll_student(course_code, next_student)
            return f"Dropped. {next_student} moved from waitlist"
        return "Dropped!"
    
    def get_all_courses(self):
        result = []
        for course in self.courses.get_all_courses():
            result.append({
                'code': course['code'],
                'name': course['name'],
                'enrolled': len(self.courses.get_enrolled(course['code'])),
                'waitlist': self.waitlists[course['code']].size()
            })
        return result
    
    def rank_students(self):
        students = self.students.get_all()
        return merge_sort_students(students)
    
    def show_status(self):
        print("\n" + "="*50)
        print("SYSTEM STATUS")
        print("="*50)
        for course in self.courses.get_all_courses():
            enrolled = len(self.courses.get_enrolled(course['code']))
            wait = self.waitlists[course['code']].size()
            print(f"{course['code']}: {enrolled}/{course['capacity']} enrolled, {wait} waiting")
        print("="*50 + "\n")


def main():
    system = RegistrationController()
    system.show_status()
    
    print("1. Register John for CS201:")
    print(system.register_student('S001', 'CS201'))
    
    print("\n2. Search for CS201:")
    print(system.search_course('CS201'))
    
    print("\n3. View all courses:")
    print(system.get_all_courses())
    
    print("\n4. Drop John from CS201:")
    print(system.drop_course('S001', 'CS201'))
    
    print("\n5. Rank students:")
    for s in system.rank_students():
        print(f"  - {s['name']} (Year {s['year']})")


if __name__ == "__main__":
    main()