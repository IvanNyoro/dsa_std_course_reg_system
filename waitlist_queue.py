# waitlist_queue.py

class Node:
    """A single student node in the waitlist queue"""
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.next = None  # Pointer to the next student in line

class WaitlistQueue:
    """A First-In-First-Out (FIFO) Queue built from scratch"""
    def __init__(self, capacity=5):
        self.front = None   # The person at the front of the line
        self.rear = None    # The person at the back of the line
        self.capacity = capacity
        self.size = 0       # Current number of people in the waitlist

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size >= self.capacity

    def enqueue(self, student_id, student_name):
        """Adds a student to the back of the waitlist"""
        if self.is_full():
            print(f"Waitlist is full! Cannot add {student_name}.")
            return False
            
        new_student = Node(student_id, student_name)
        
        if self.rear is None:
            # If queue is empty, the new student is both front and rear
            self.front = self.rear = new_student
        else:
            # Add the new student behind the current rear, then update rear
            self.rear.next = new_student
            self.rear = new_student
            
        self.size += 1
        print(f"✅ Enqueued: {student_name} (ID: {student_id}) to the waitlist.")
        return True

    def dequeue(self):
        """Removes and returns the student at the front of the waitlist"""
        if self.is_empty():
            print("Waitlist is empty. No one to dequeue.")
            return None
            
        temp = self.front
        self.front = temp.next # Move the front pointer back one person
        
        # If the queue is now empty, rear must also be None
        if self.front is None:
            self.rear = None
            
        self.size -= 1
        print(f" Dequeued: {temp.student_name} is moving from waitlist to enrolled!")
        return temp

# --- TEST CODE FOR PROGRESS CHECK ---
if __name__ == "__main__":
    print("--- TESTING WAITLIST QUEUE ---")
    dsa_waitlist = WaitlistQueue(capacity=3)
    
    # Test adding students
    dsa_waitlist.enqueue("S001", "Alice")
    dsa_waitlist.enqueue("S002", "Bob")
    dsa_waitlist.enqueue("S003", "Charlie")
    
    # Test capacity limit
    dsa_waitlist.enqueue("S004", "David") # Should fail
    
    # Test removing students (FIFO check)
    dsa_waitlist.dequeue() # Alice should come out first
    dsa_waitlist.dequeue() # Then Bob