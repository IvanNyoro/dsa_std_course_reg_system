"""
SNo. 220526: ALGORITHMS INTEGRATION
DFS + Binary Search + Merge Sort
"""

def dfs_check_prerequisites(course_code, completed_courses, prereq_tree, visited=None):
    """DFS: Check if student has ALL prerequisites"""
    if visited is None:
        visited = set()
    
    required = prereq_tree.get_prerequisites(course_code)
    if not required:
        return True
    
    for prereq in required:
        if prereq in visited:
            continue
        visited.add(prereq)
        if prereq not in completed_courses:
            return False
        if not dfs_check_prerequisites(prereq, completed_courses, prereq_tree, visited):
            return False
    return True


def binary_search_course(courses_list, target_code):
    """Binary Search: Find course by code O(log n)"""
    left, right = 0, len(courses_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if courses_list[mid]['code'] == target_code:
            return courses_list[mid]
        elif target_code < courses_list[mid]['code']:
            right = mid - 1
        else:
            left = mid + 1
    return None


def merge_sort_students(students):
    """Merge Sort: Rank students by Year → GPA"""
    if len(students) <= 1:
        return students
    mid = len(students) // 2
    left = merge_sort_students(students[:mid])
    right = merge_sort_students(students[mid:])
    return _merge(left, right)


def _merge(left, right):
    """Merge two sorted lists"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]['year'] > right[j]['year']:
            result.append(left[i]); i += 1
        elif left[i]['year'] < right[j]['year']:
            result.append(right[j]); j += 1
        else:
            if left[i].get('gpa', 0) >= right[j].get('gpa', 0):
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result