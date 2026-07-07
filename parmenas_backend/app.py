# MEMBER 4: BACKEND CONTROLLER - TERMINAL VERSION

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Imports 
from ivan_ds.waitlist_queue import WaitlistQueue
from ivan_ds.course_list import RegisteredCoursesList
from ivan_ds.std_hashmap import StudentHashMap

from algorithms import dfs_check_prerequisites, binary_search_course, merge_sort_students


class RegistrationController:
    def __init__(self):
        self.students = StudentHashMap()
        self.courses = {}
        self.student_courses = {}
        self.waitlists = {}
        self.prereqs = {}
        self.student_data = {}
        self._load_dummy_data()
        print("✅ System Ready!")
    
    def _load_dummy_data(self):
        # Simple hardcoded data
        self.courses = {
            'CS101': {'name': 'Intro Programming', 'capacity': 2},
            'CS201': {'name': 'Data Structures', 'capacity': 2},
            'CS301': {'name': 'Algorithms', 'capacity': 1},
        }
        self.prereqs = {'CS201': ['CS101'], 'CS301': ['CS201']}
        
        # Students
        for sid, name, year, gpa in [
            ('S001', 'Parmenas Ngugi', 4, 3.8),
            ('S002', 'Jane Smith', 3, 3.5),
            ('S003', 'Alice Johnson', 2, 3.2),
            ('S004', 'Bob Williams', 4, 2.9),
        ]:
            self.students.add_student(sid, name)
            self.student_data[sid] = {'year': year, 'gpa': gpa, 'completed': ['CS101'] if sid == 'S001' else []}
            self.student_courses[sid] = RegisteredCoursesList()
        
        # Waitlists for courses
        for course in self.courses:
            self.waitlists[course] = WaitlistQueue(capacity=3)
    
    def get_prerequisites(self, course):
        return self.prereqs.get(course, [])
    
    # FUNCTIONS 
    
    def register_student(self, student_id, course_code):
        """Register or waitlist"""
        if not self.students.find_student(student_id):
            return "Student not found"
        if course_code not in self.courses:
            return "Course not found"
        
        # Check prerequisites
        if not dfs_check_prerequisites(course_code, self.student_data[student_id]['completed'], self):
            return "Missing prerequisites"
        
        # Check if already registered
        current = self.student_courses[student_id].head
        while current:
            if current.course_code == course_code:
                return "Already registered"
            current = current.next
        
        # Count enrolled
        enrolled = 0
        for sid in self.student_courses:
            c = self.student_courses[sid].head
            while c:
                if c.course_code == course_code:
                    enrolled += 1
                c = c.next
        
        if enrolled < self.courses[course_code]['capacity']:
            self.student_courses[student_id].add_course(course_code, self.courses[course_code]['name'])
            return "Registered!"
        else:
            self.waitlists[course_code].enqueue(student_id, self.students.find_student(student_id))
            return f"Added to waitlist (Position: {self.waitlists[course_code].size})"
    
    def search_course(self, course_code):
        """Binary Search"""
        courses = [{'code': c, 'name': info['name'], 'capacity': info['capacity']} 
                   for c, info in self.courses.items()]
        courses.sort(key=lambda x: x['code'])
        return binary_search_course(courses, course_code)
    
    def drop_course(self, student_id, course_code):
        """Drop and move waitlist"""
        if course_code not in self.courses:
            return "Course not found"
        
        self.student_courses[student_id].drop_course(course_code)
        
        if not self.waitlists[course_code].is_empty():
            next_student = self.waitlists[course_code].dequeue()
            if next_student:
                self.student_courses[next_student.student_id].add_course(
                    course_code, self.courses[course_code]['name']
                )
                return f"Dropped. {next_student.student_name} moved from waitlist"
        return "Dropped!"
    
    def get_all_courses(self):
        """View all courses"""
        result = []
        for code, info in self.courses.items():
            enrolled = 0
            for sid in self.student_courses:
                c = self.student_courses[sid].head
                while c:
                    if c.course_code == code:
                        enrolled += 1
                    c = c.next
            result.append({
                'code': code,
                'name': info['name'],
                'enrolled': enrolled,
                'waitlist': self.waitlists[code].size,
                'seats_left': info['capacity'] - enrolled
            })
        return result
    
    def rank_students(self):
        """Rank students"""
        student_list = []
        for sid, data in self.student_data.items():
            student_list.append({
                'id': sid,
                'name': self.students.find_student(sid) or 'Unknown',
                'year': data['year'],
                'gpa': data['gpa']
            })
        return merge_sort_students(student_list)
    
    def show_status(self):
        """Show status"""
        print("\n" + "="*50)
        print("SYSTEM STATUS")
        print("="*50)
        for c in self.get_all_courses():
            print(f"{c['code']}: {c['enrolled']}/{self.courses[c['code']]['capacity']} enrolled, {c['waitlist']} waiting")
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