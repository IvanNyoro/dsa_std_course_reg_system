# course_list.py

class CourseNode:
    """A single node in the student's registered courses linked list"""
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name
        self.next = None  # Pointer to the next course in the student's list

class RegisteredCoursesList:
    """A linked list to manage a student's registered courses"""
    def __init__(self):
        self.head = None # The first course in the list (starts empty)

    def add_course(self, course_code, course_name):
        """Adds a new course to the end of the linked list"""
        new_course = CourseNode(course_code, course_name)
        
        # If list is empty, make this the first course (head)
        if self.head is None:
            self.head = new_course
            return

        # else, traverse to the end of the list and attach it
        current = self.head
        while current.next:
            current = current.next
        current.next = new_course

    def drop_course(self, course_code):
        """Removes a course from the linked list based on its code"""
        current = self.head
        previous = None # Keep track of the node before current to help with removal

        # Loop through until we find the course to drop
        while current and current.course_code != course_code:
            previous = current
            current = current.next

        # Case 1: The course wasn't found in the list
        if current is None:
            return False

        # Case 2: The course to drop is the very first course (head)
        if previous is None:
            self.head = current.next
        else:
            # Case 3: Cut out the current node by pointing previous straight to next
            previous.next = current.next

        return True # Successfully dropped the course
    
    def get_all_courses(self):
        """Helper for Member 4 to pull list data and render it onto the HTML table"""
        courses = []
        current = self.head
        while current:
            courses.append({"code": current.course_code, "name": current.course_name})
            current = current.next
        return courses


# --- TEST CODE FOR PROGRESS CHECK ---
if __name__ == "__main__":
    print("--- TESTING COURSE LINKED LIST ---")
    ivan_courses = RegisteredCoursesList()
    
    # 1. Add courses
    ivan_courses.add_course("ICS 2.1", "Data Structures and Algorithms")
    ivan_courses.add_course("ICS 2.2", "Database Systems")
    
    # 2. Show schedule
    print(f"Current schedule: {ivan_courses.get_all_courses()}")
    
    # 3. Drop a course
    ivan_courses.drop_course("ICS 2.2")
    
    # 4. Show schedule again to prove it dropped successfully
    print(f"Updated schedule: {ivan_courses.get_all_courses()}")