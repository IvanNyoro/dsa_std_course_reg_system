class StudentNode:
    """A node representing a student profile in the system"""
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.courses = None # Pointer to the student's registered courses list
        self.next = None  # Pointer to the next node if a collision happens

class StudentHashMap:
    """A Custom Hash Map for O(1) student lookups"""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets = [None] * self.capacity

    def _hash_function(self, student_id):
        """Custom hash: sums ASCII values of the ID string"""
        return sum(ord(char) for char in str(student_id)) % self.capacity

    def insert(self, student_id, student_name):
        """Inserts or updates a student profile"""
        index = self._hash_function(student_id)
        new_node = StudentNode(student_id, student_name)
        
        # If the bucket slot is completely empty, drop the new student here
        if self.buckets[index] is None:
            self.buckets[index] = new_node
            return True
            
        # Collision handling: traverse the linked list at this bucket
        current = self.buckets[index]
        while current:
            # If the student ID already exists, UPDATE their name instead of duplicating
            if current.student_id == student_id:
                current.student_name = student_name 
                return True
            if current.next is None:
                break
            current = current.next
        
        # If we reached the end of the chain and didn't find the ID, append the new node
        current.next = new_node
        return True

    def get(self, student_id):
        """Searches for a student in O(1) average time complexity"""
        index = self._hash_function(student_id)
        current = self.buckets[index]

        # Traverse the bucket in case of collisions
        while current:
            if current.student_id == student_id:
                return current
            current = current.next
        return None # Student not found

# --- TEST CODE FOR PROGRESS CHECK ---
if __name__ == "__main__":
    registry = StudentHashMap()
    registry.insert("220886", "Ivan")
    student = registry.get("220886")
    print(f"Verified: {student.student_name} is in the system.")