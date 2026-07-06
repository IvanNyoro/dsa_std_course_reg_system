# member2_validation/algorithms.py
"""
Member 2: Core Algorithms Engineer
Focus: Backend Processing Logic, Graph Traversal & Waitlist Promotion

This module contains the custom data structures and traversal algorithms 
required to validate student registration eligibility based on course prerequisites,
as well as the logic to automatically promote students from waitlists on course drop.
"""

class PrerequisiteGraph:
    """
    A Custom Directed Graph class implemented from scratch.
    Nodes represent Course Codes (strings), and directed edges represent prerequisite dependencies.
    If course B has course A as a prerequisite, we store B -> A.
    """
    def __init__(self):
        # We use a custom adjacency list represented by a dictionary
        self.adj_list = {}

    def add_course(self, course_code):
        """Adds a course to the graph if it doesn't already exist."""
        if course_code not in self.adj_list:
            self.adj_list[course_code] = []

    def add_prerequisite(self, course_code, prereq_code):
        """
        Creates a directed edge indicating that 'prereq_code' is a prerequisite for 'course_code'.
        Ensures both course nodes are present in the graph first.
        """
        self.add_course(course_code)
        self.add_course(prereq_code)
        
        # Avoid duplicate edges
        if prereq_code not in self.adj_list[course_code]:
            self.adj_list[course_code].append(prereq_code)

    def get_direct_prerequisites(self, course_code):
        """Returns the immediate prerequisites for a course."""
        return self.adj_list.get(course_code, [])

    def display_graph(self):
        """Utility method to print the adjacency list in a readable ledger style."""
        print("\n--- Prerequisite Adjacency Ledger ---")
        for course, prereqs in self.adj_list.items():
            if prereqs:
                print(f"[{course}] requires: {', '.join(prereqs)}")
            else:
                print(f"[{course}] has no prerequisites.")
        print("--------------------------------------\n")


# ==========================================
# CORE ALGORITHMS: GRAPH TRAVERSALS (DFS/BFS)
# ==========================================

def dfs_get_all_prerequisites(graph, start_course):
    """
    Traverses the prerequisite graph recursively using Depth-First Search (DFS)
    to compile a complete list of all ancestor prerequisite courses (both direct and indirect).
    
    Time Complexity: O(V + E) where V = Vertices (Courses) and E = Edges (Prerequisites).
    Space Complexity: O(V) due to the call stack and visited tracker.
    """
    visited = set()
    all_prereqs = []

    def dfs(course):
        for prereq in graph.get_direct_prerequisites(course):
            if prereq not in visited:
                visited.add(prereq)
                all_prereqs.append(prereq)
                dfs(prereq)  # Recurse deeper into the prerequisite chain

    dfs(start_course)
    return all_prereqs


def bfs_get_all_prerequisites(graph, start_course):
    """
    Traverses the prerequisite graph iteratively using Breadth-First Search (BFS)
    to compile a complete list of all ancestor prerequisite courses (both direct and indirect).
    Uses a simple list-based queue to satisfy from-scratch implementation.
    
    Time Complexity: O(V + E) where V = Vertices (Courses) and E = Edges (Prerequisites).
    Space Complexity: O(V) for the queue and visited tracker.
    """
    visited = set()
    all_prereqs = []
    
    # Custom queue initialization (FIFO)
    queue = [start_course]
    
    while len(queue) > 0:
        # Dequeue the first element (O(V) in worst case for list pop, 
        # but suitable for custom course hierarchy size)
        current = queue.pop(0)
        
        for prereq in graph.get_direct_prerequisites(current):
            if prereq not in visited:
                visited.add(prereq)
                all_prereqs.append(prereq)
                queue.append(prereq)
                
    return all_prereqs


# ==========================================
# REGISTRATION ELIGIBILITY VALIDATION
# ==========================================

def validate_enrollment(graph, course_code, student_completed_courses):
    """
    Validates if a student is eligible to enroll in a target course.
    Uses DFS traversal to determine all required prerequisites, then cross-checks
    them against the list of courses the student has completed.
    
    Parameters:
    - graph: PrerequisiteGraph instance.
    - course_code: Code of the target course (e.g. "ICS 2.1").
    - student_completed_courses: List/Set of course codes the student has completed.
    
    Returns:
    - (is_eligible, missing_prerequisites)
      - is_eligible: Boolean (True if student has completed all requirements, else False)
      - missing_prerequisites: List of prerequisite course codes the student is missing
    """
    # 1. Fetch all required courses in the prerequisite chain using DFS
    required_prereqs = dfs_get_all_prerequisites(graph, course_code)
    
    # Convert student completed courses to a set for O(1) average lookup time
    completed_set = set(student_completed_courses)
    
    missing_prereqs = []
    for prereq in required_prereqs:
        if prereq not in completed_set:
            missing_prereqs.append(prereq)
            
    # Eligible if there are zero missing prerequisites
    is_eligible = len(missing_prereqs) == 0
    return is_eligible, missing_prereqs


# ==========================================
# WAITLIST AUTOMATIC PROMOTION ALGORITHM
# ==========================================

def promote_waitlisted_student(course_code, waitlist_queue, enroll_callback):
    """
    Automatically promotions the first student in the course's waitlist
    to enrolled status if a seat becomes available (e.g. when someone drops).
    
    Parameters:
    - course_code: Code of the course (string).
    - waitlist_queue: Member 1's custom WaitlistQueue instance.
    - enroll_callback: A function/method to call to execute the enrollment.
      Signature: enroll_callback(student_id, student_name, course_code)
      
    Returns:
    - promoted_student_node: Node of the student who was promoted, or None if waitlist was empty.
    """
    if waitlist_queue.is_empty():
        print(f"Waitlist for {course_code} is empty. No promotion required.")
        return None
        
    # Dequeue the first student from the FIFO waitlist queue
    promoted_student = waitlist_queue.dequeue()
    
    if promoted_student:
        print(f"🔄 [Promotion System] Student {promoted_student.student_name} (ID: {promoted_student.student_id}) "
              f"is being promoted to {course_code} from the waitlist.")
        
        # Execute the callback to update the central records/enrolled list
        enroll_callback(promoted_student.student_id, promoted_student.student_name, course_code)
        return promoted_student
        
    return None
