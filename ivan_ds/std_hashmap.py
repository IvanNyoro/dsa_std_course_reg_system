class HashNode:
    """A node to store student data and handle collisions (Separate Chaining)"""
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.next = None  # Pointer to the next node if a collision happens

class StudentHashMap:
    """A Custom Hash Map for O(1) student lookups"""
    def __init__(self, capacity=10):
        self.capacity = capacity
        # Create an array of empty buckets
        self.buckets = [None] * self.capacity

    def _hash_function(self, student_id):
        """Converts a student ID string into an array index"""
        hash_value = 0
        for char in student_id:
            hash_value += ord(char) # Get ASCII value of character
        return hash_value % self.capacity

    def add_student(self, student_id, name):
        """Inserts a student into the hash map"""
        index = self._hash_function(student_id)
        new_student = HashNode(student_id, name)

        # If bucket is empty, place student there
        if self.buckets[index] is None:
            self.buckets[index] = new_student
            print(f"Added {name} at index {index}")
        else:
            # Collision occurred! Use linked list chaining to add to the end
            current = self.buckets[index]
            while current.next:
                current = current.next
            current.next = new_student
            print(f"Collision at index {index}! Chained {name} to existing bucket.")

    def find_student(self, student_id):
        """Searches for a student in O(1) average time complexity"""
        index = self._hash_function(student_id)
        current = self.buckets[index]

        # Traverse the bucket in case of collisions
        while current:
            if current.student_id == student_id:
                print(f"Found Student: {current.name} (ID: {current.student_id})")
                return current.name
            current = current.next
            
        print(f"Student with ID {student_id} not found.")
        return None

# --- TEST CODE FOR PROGRESS CHECK ---
if __name__ == "__main__":
    print("--- TESTING STUDENT HASH MAP ---")
    db = StudentHashMap(capacity=5)
    
    # Add your group members!
    db.add_student("220886", "Nyoro Ivan Leo")
    db.add_student("220697", "Njugi Aaron Kiuna")
    db.add_student("220526", "Parmenas Ngugi")
    
    # Test instant O(1) search
    print("\n--- Searching ---")
    db.find_student("220886") # Should find Ivan instantly
    db.find_student("999999") # Should fail