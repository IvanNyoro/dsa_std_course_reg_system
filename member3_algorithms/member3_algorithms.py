# Member 3: Data Processing & Optimization Specialist


class Course:
    def __init__(self, course_id, course_name, capacity):
        self.course_id = course_id        
        self.course_name = course_name    
        self.capacity = capacity          

    def __repr__(self):
        return f"Course(ID: {self.course_id}, Name: '{self.course_name}', Cap: {self.capacity})"


class Student:
    def __init__(self, student_id, name, year_of_study):
        self.student_id = student_id      
        self.name = name                  
        self.year_of_study = year_of_study  

    def __repr__(self):
        return f"Student(ID: {self.student_id}, Name: '{self.name}', Year: {self.year_of_study})"


# --- CORE ALGORITHMS ---

def binary_search_courses(course_list, target_id):
    """Custom Binary Search to locate a Course object by its unique ID."""
    low = 0
    high = len(course_list) - 1

    while low <= high:
        mid = (low + high) // 2
        current_course = course_list[mid]

        if current_course.course_id == target_id:
            return current_course
        elif current_course.course_id < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None


def merge_sort_students(student_list):
    """Custom Merge Sort to prioritize students by Year of Study (Descending)."""
    if len(student_list) <= 1:
        return student_list

    mid = len(student_list) // 2
    left_half = student_list[:mid]
    right_half = student_list[mid:]

    left_sorted = merge_sort_students(left_half)
    right_sorted = merge_sort_students(right_half)

    return _merge(left_sorted, right_sorted)


def _merge(left, right):
    """Helper utility to merge two sorted arrays based on student priority."""
    sorted_list = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].year_of_study >= right[j].year_of_study:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1

    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list


# TERMINAL PROGRESS CHECK DEMO 

if __name__ == "__main__":
    print("--- 🔍 Member 3: Running Progress Check Demo ---")
    
    # Test Binary Search
    mock_courses = [
        Course(101, "Intro to Programming", 50),
        Course(102, "Data Structures & Algorithms", 40),
        Course(201, "Database Systems", 30)
    ]
    print(f"Searching for Course 201...")
    print(f"Result: {binary_search_courses(mock_courses, 201)}")

    # Test Merge Sort
    mock_students = [
        Student(1, "Alice", 2),
        Student(2, "Bob", 4),
        Student(3, "Charlie", 1)
    ]
    print(f"\nSorting Students by Year...")
    print(f"Result: {merge_sort_students(mock_students)}")
    