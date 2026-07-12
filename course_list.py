# course_list.py

class CourseNode:
    """A single course node selected by a student"""
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name
        self.next = None  # Pointer to the next course in the student's list

class RegisteredCoursesList:
    """A Singly Linked List to track a student's chosen courses"""
    def __init__(self):
        self.head = None # The first course in the list (starts empty)

    def add_course(self, course_code, course_name):
        """Adds a course to the end of the linked list"""
        new_course = CourseNode(course_code, course_name)
        
        # If list is empty, make this the first course (head)
        if self.head is None:
            self.head = new_course
            print(f"Added {course_code} as the first course.")
            return

        # Otherwise, traverse to the end of the list and attach it
        current = self.head
        while current.next:
            current = current.next
        current.next = new_course
        print(f"Added {course_code} to the schedule.")

    def drop_course(self, course_code):
        """Removes a specific course from the linked list"""
        current = self.head
        previous = None

        # Loop through until we find the course to drop
        while current and current.course_code != course_code:
            previous = current
            current = current.next

        # Case 1: The course wasn't found in the list
        if current is None:
            print(f"Cannot drop {course_code}. You are not registered for it.")
            return

        # Case 2: The course to drop is the very first course (head)
        if previous is None:
            self.head = current.next
        else:
            # Case 3: Cut out the current node by pointing previous straight to next
            previous.next = current.next
            
        print(f"Successfully dropped {course_code}.")

    def display_schedule(self):
        """Prints all currently registered courses"""
        current = self.head
        if not current:
            print("Schedule is currently empty.")
            return
            
        print("\n--- Current Course Schedule ---")
        while current:
            print(f"{current.course_code}: {current.course_name}")
            current = current.next
        print("-------------------------------\n")


# --- TEST CODE FOR PROGRESS CHECK ---
if __name__ == "__main__":
    print("--- TESTING COURSE LINKED LIST ---")
    ivan_courses = RegisteredCoursesList()
    
    # 1. Add courses
    ivan_courses.add_course("ICS 2.1", "Data Structures and Algorithms")
    ivan_courses.add_course("ICS 2.2", "Database Systems")
    
    # 2. Show schedule
    ivan_courses.display_schedule()
    
    # 3. Drop a course
    ivan_courses.drop_course("ICS 2.2")
    
    # 4. Show schedule again to prove it dropped successfully
    ivan_courses.display_schedule()