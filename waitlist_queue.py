# waitlist_queue.py

class Node:
    """A single node in the waitlist queue"""
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.next = None 

class WaitlistQueue:
    """A Queue to manage students waiting for course enrollment"""
    def __init__(self, capacity=5):
        self.front = None
        self.rear = None
        self.capacity = capacity
        self.size = 0 # Current number of people in the waitlist

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size >= self.capacity

    def enqueue(self, student_id, student_name):
        """Adds a student to the back of the waitlist"""
        if self.is_full():
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
        return True

    def dequeue(self):
        """Removes and returns the student at the front of the waitlist"""
        if self.is_empty():
            return None
            
        temp = self.front
        self.front = temp.next # Move the front pointer back one person
        
        # If the queue is now empty, rear must also be None
        if self.front is None:
            self.rear = None
            
        self.size -= 1
        return temp # returns student node to be registered

# --- TEST CODE FOR PROGRESS CHECK ---
if __name__ == "__main__":
    dsa_waitlist = WaitlistQueue(capacity=2)
    dsa_waitlist.enqueue("S001", "Alice")