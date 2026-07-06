# member2_validation/run_demo.py
"""
Member 2: Core Algorithms Engineer
Terminal Demo & Progress Check Runner

This script demonstrates:
1. Prerequisite Graph traversal using DFS and BFS.
2. Eligibility validation (blocking students missing prerequisites).
3. Automatic waitlist promotion when a student drops a full course.
"""

import sys
import os
import io

# Force stdout/stderr to use UTF-8 encoding to avoid Windows console encoding errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add parent directory to sys.path to enable loading ivan_ds
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from ivan_ds.waitlist_queue import WaitlistQueue
except ImportError:
    print("Error: Could not import WaitlistQueue from ivan_ds.waitlist_queue.")
    print("Please ensure you are running this from the correct path, and the ivan_ds folder contains waitlist_queue.py.")
    sys.exit(1)

from algorithms import (
    PrerequisiteGraph,
    dfs_get_all_prerequisites,
    bfs_get_all_prerequisites,
    validate_enrollment,
    promote_waitlisted_student
)


def run_traversal_demo(graph):
    print("\n" + "="*50)
    print(" 1. DEMONSTRATING GRAPH TRAVERSAL (DFS vs BFS)")
    print("="*50)
    
    # Visualizing Graph
    graph.display_graph()
    
    # Traversal from Advanced Web Development (ICS 2.2)
    course = "ICS 2.2"
    print(f"Traversing prerequisite tree for {course}...")
    
    dfs_result = dfs_get_all_prerequisites(graph, course)
    bfs_result = bfs_get_all_prerequisites(graph, course)
    
    print(f"DFS Traversal Path (Depth-First order of requirements): {dfs_result}")
    print(f"BFS Traversal Path (Breadth-First order of requirements): {bfs_result}")


def run_validation_demo(graph):
    print("\n" + "="*50)
    print(" 2. DEMONSTRATING ENROLLMENT ELIGIBILITY VALIDATION")
    print("="*50)
    
    # Mock students and their transcripts (completed courses)
    student_records = {
        "S001": {"name": "Alice Njuguna", "completed": ["ICS 1.1", "ICS 1.2", "ICS 2.1"]},
        "S002": {"name": "Bob Mwangi", "completed": ["ICS 1.1"]},
        "S003": {"name": "Charlie Otieno", "completed": []}
    }
    
    target_course = "ICS 2.2"  # Requires: ICS 2.1 and ICS 1.2 (which requires ICS 1.1)
    
    for student_id, data in student_records.items():
        name = data["name"]
        completed = data["completed"]
        
        print(f"\nStudent: {name} (ID: {student_id})")
        print(f"Transcript (Completed Courses): {completed if completed else 'None'}")
        print(f"Attempting to register for: {target_course}")
        
        eligible, missing = validate_enrollment(graph, target_course, completed)
        
        if eligible:
            print(f"✅ Enrollment status: APPROVED! All prerequisites satisfied.")
        else:
            print(f"❌ Enrollment status: BLOCKED!")
            print(f"   Reason: Missing prerequisite course(s): {missing}")


def run_waitlist_promotion_demo(graph):
    print("\n" + "="*50)
    print(" 3. DEMONSTRATING AUTOMATIC WAITLIST PROMOTION")
    print("="*50)
    
    # Mock Course state
    course_code = "ICS 2.2"
    course_name = "Advanced Web Development"
    capacity = 2
    
    # Currently enrolled students
    enrolled_students = ["S001 (Alice)", "S004 (David)"]
    print(f"Course: {course_code} - {course_name}")
    print(f"Capacity: {capacity} | Enrolled students: {enrolled_students} (Seats FULL)")
    
    # Setup waitlist queue (Member 1's custom Queue)
    waitlist = WaitlistQueue(capacity=3)
    
    # Student Eve wants to register.
    # Eve has taken the prerequisites
    eve_completed = ["ICS 1.1", "ICS 1.2", "ICS 2.1"]
    eve_id = "S005"
    eve_name = "Eve Wanjiku"
    
    print(f"\nStudent: {eve_name} (ID: {eve_id}) attempts to register...")
    eligible, missing = validate_enrollment(graph, course_code, eve_completed)
    
    if eligible:
        print("✅ Prerequisite check passed.")
        if len(enrolled_students) >= capacity:
            print(f"⚠️ Course is FULL. Enqueuing {eve_name} to the waitlist queue...")
            waitlist.enqueue(eve_id, eve_name)
        else:
            enrolled_students.append(f"{eve_id} ({eve_name})")
            print(f"✅ Enrolled {eve_name} directly.")
    else:
        print(f"❌ Blocked: missing {missing}")
        
    print(f"\nWaitlist queue size: {waitlist.size}")
    
    # Callback function to perform actual enrollment on promotion
    def enroll_student_callback(student_id, student_name, course):
        enrolled_students.append(f"{student_id} ({student_name})")
        print(f"🎉 Success: {student_name} is now registered in course {course}!")
        print(f"Updated Enrolled List: {enrolled_students}")

    # Now, a student drops the course
    dropping_student = "S004 (David)"
    print(f"\n🛑 Action: David ({dropping_student}) drops {course_code}!")
    enrolled_students.remove(dropping_student)
    print(f"David removed. Updated Enrolled List: {enrolled_students} (1 empty slot!)")
    
    # Trigger promotion algorithm
    print("Triggering waitlist promotion check...")
    promoted = promote_waitlisted_student(course_code, waitlist, enroll_student_callback)
    
    if promoted:
        print(f"Result: {promoted.student_name} successfully promoted.")
    else:
        print("Result: No one was promoted.")
        
    print(f"\nFinal waitlist queue size: {waitlist.size}")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Setup Graph representing Course Prerequisites
    # Structure:
    # ICS 1.1 -> ICS 1.2 -> ICS 2.1 -> ICS 2.2
    # Also, ICS 1.2 -> ICS 2.2 (direct prerequisite requirement as well)
    graph = PrerequisiteGraph()
    
    # Adding nodes and relationships
    graph.add_prerequisite("ICS 1.2", "ICS 1.1")  # ICS 1.2 requires ICS 1.1
    graph.add_prerequisite("ICS 2.1", "ICS 1.2")  # ICS 2.1 requires ICS 1.2
    graph.add_prerequisite("ICS 2.2", "ICS 2.1")  # ICS 2.2 requires ICS 2.1
    graph.add_prerequisite("ICS 2.2", "ICS 1.2")  # ICS 2.2 requires ICS 1.2
    
    # 1. Traversal Demo
    run_traversal_demo(graph)
    
    # 2. Validation Demo
    run_validation_demo(graph)
    
    # 3. Promotion Demo
    run_waitlist_promotion_demo(graph)
