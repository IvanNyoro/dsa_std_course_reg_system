# Member 2 Workspace: Core Algorithms (Validation & Traversal)
**Role:** Core Algorithms Engineer

This folder contains the graph traversal algorithms for prerequisite validation and the automatic waitlist promotion algorithm for the **Student Course Registration System**.

## 📋 Table of Contents
1. [Overview of Responsibilities](#-overview-of-responsibilities)
2. [Graph Representation of Prerequisites](#-graph-representation-of-prerequisites)
3. [Algorithm Design](#-algorithm-design)
    - [Prerequisite Validation (DFS & BFS)](#prerequisite-validation-dfs--bfs)
    - [Waitlist Promotion](#waitlist-promotion)
4. [Big-O Complexity Analysis](#-big-o-complexity-analysis)
5. [Running the Terminal Demo](#-running-the-terminal-demo)

---

## 👤 Overview of Responsibilities
As the **Core Algorithms Engineer (Member 2)**, my focus is backend validation logic and graph traversal to ensure correct system integrity.
* **Prerequisite Validation:** Traverse the course prerequisite graph using Depth-First Search (DFS) or Breadth-First Search (BFS) to compile all required courses (both direct and indirect). If a student has not completed every course in the prerequisite chain, they are blocked from registering.
* **Waitlist Promotion:** Implement logic that automatically dequeues the next student in line from a course's waitlist (FIFO Queue) and enrolls them if a student currently in the course drops it.

---

## 🕸️ Graph Representation of Prerequisites
Since Member 1's custom directed graph has not yet been pushed, this folder includes a custom `PrerequisiteGraph` class. 
* **Structure:** A directed graph represented as an adjacency list.
* **Direction:** Edges are directed from a course to its prerequisites (e.g., `ICS 2.2 -> ICS 2.1` and `ICS 2.2 -> ICS 1.2`).
* **acyclic (DAG):** Pre-requisite structures are Directed Acyclic Graphs (DAGs) to prevent circular dependencies.

---

## 🛠️ Algorithm Design

### Prerequisite Validation (DFS & BFS)
To validate if a student is eligible for a course:
1. We check if the course exists in the `PrerequisiteGraph`.
2. We run **DFS** (recursive) or **BFS** (iterative) traversal from the target course to compile all ancestors (both direct prerequisites and prerequisites of those prerequisites).
3. We compare the set of all required prerequisite courses against the student's completed courses list.
4. If there is a mismatch (i.e. missing prerequisites), registration is blocked and the missing course codes are returned.

### Waitlist Promotion
When a student drops a course:
1. The system removes the dropping student from the course's enrolled list.
2. If there are students in that course's waitlist queue (FIFO), we call `promote_waitlisted_student`.
3. The promotion algorithm dequeues the front student node from the `WaitlistQueue` and triggers a callback function to add them to the enrolled list.

---

## 📊 Big-O Complexity Analysis

| Algorithm / Operation | Time Complexity | Space Complexity | Explanation |
| :--- | :--- | :--- | :--- |
| **Prerequisite Traversal (DFS/BFS)** | $O(V + E)$ | $O(V)$ | $V$ represents the number of courses (vertices), and $E$ represents prerequisite connections (edges). Each node and edge is visited at most once. The space complexity is bounded by the recursion stack (for DFS), queue (for BFS), and the visited set. |
| **Eligibility Validation** | $O(V + E + P)$ | $O(V + P)$ | We run the traversal ($O(V + E)$) to get all $P$ prerequisites, convert the student's completed courses to a set ($O(S)$ where $S$ is size of transcript), and check each required prerequisite in $O(1)$ average time. Thus, it scales linearly with the graph size and student history size. |
| **Waitlist Promotion** | $O(1)$ | $O(1)$ | Dequeuing from Member 1's custom `WaitlistQueue` (implemented with a singly linked list with a front pointer) is a constant time operation. Pointer updates and callback trigger require $O(1)$ auxiliary space. |

---

## 🚀 Running the Terminal Demo
A progress check and integration demo runner has been written in `run_demo.py`. It runs a mock prerequisite validation and waitlist promotion workflow.

To run the demo, run the following command in your terminal from this folder:
```bash
python run_demo.py
```
