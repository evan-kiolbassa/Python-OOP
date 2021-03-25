'''
A recursive function is a function that
calls itself. To stop recursion from continuing to infinity,
a base case assure it eventually stops. 
The recursion comes from the fact that we use 
the same algorithm to solve those simpler instances. The base case happens when 
the problem becomes simple enough that we don't need to break it down further to solve it.
The base case is necessary to ensure your program doesn't run out of memory.
A call stack is a stack data structure that stores information about the active subroutines 
of acomputer program.
A stack overflow occurs if the call stack pointer exceeds the stack bound. 
Stack overflow is acommon cause of infinite recursion.•To solve a problem recursively, we 
need to express it as a combination of solutions to smallerinstances of the same problem. 
We stop decomposing the problem when the problem becomes small enough that we can solve it 
directly. This is the base.
'''
import os
def recursive_sum(values):    
    # Base case: the list is empty    
    if not values:        
        return 0    
    # General case: the list is not empty    
    return values[0] + recursive_sum(values[1:])
'''
Since the number of disks in each subproblem is smaller, 
all subproblems eventually contain a single disk. 
These subproblems with a single disk are solveable with a single move. 
The combination of all of these moves results in a solution to the original puzzle.
'''
def solve_hanoi(num_disks, first_peg, middle_peg, last_peg):    
    if num_disks == 1:        
        # Base case        
        print("Move the top disk from peg {} to peg {}.".format(first_peg, last_peg))    
    else:        
        # General Case     
        # Move a stack of size num_disks - 1 from first_peg to middle_peg using last_peg as temporary peg.   
        solve_hanoi(num_disks - 1, first_peg, last_peg, middle_peg) 
        # Single disk from first_peg to last_peg using middle_peg as intermediate peg.       
        solve_hanoi(1, first_peg, middle_peg, last_peg)  
        # Move a stack of size num_disks - 1 from middle_peg to last_peg using first_peg as temporary peg.      
        solve_hanoi(num_disks - 1, middle_peg, first_peg, last_peg)


'''
os.listdir(): Given a path, it returns a list with all of the contents of that path.
os.path.isdir(): Given a path, returns True if the paths is a folder and False otherwise.
os.path.join(): Concatenates two paths into a proper path.


Base case: use the os.path.isdir() function to check whether current_path is a directory. If it isn't, then print the value of current_path.
General case: else, if current_path is a directory then, for each name in os.listdir(current_path):
Use the os.path.join() function to join current_path and name.
Recursively call the list_files() function on the joined path.
'''
def list_files(current_path):    
    #Base case    
    if not os.path.isdir(current_path):        
        print(current_path)    
    else:        
        # General case        
        for fn in os.listdir(current_path):            
            fn_path = os.path.join(current_path, fn)            
            list_files(fn_path)


def merge_sorted_lists(list1, list2):
    index1 = 0
    index2 = 0
    merged_list = []
    # Collect the font value while both lists are not empty
    while index1 < len(list1) and index2 < len(list2):
        if list1[index1] < list2[index2]:
            merged_list.append(list1[index1])
            index1 += 1
        else:
            merged_list.append(list2[index2])
            index2 += 1
    # Add remaining values
    merged_list += list1[index1:]
    merged_list += list2[index2:]
    return merged_list
'''
The goal of the merge sort algorithm is to first divide up an unsorted list into a bunch 
of smaller sorted lists and then merge them all to create a sorted list.
The time complexity for merge sort is O(n × log(n))

Base case: 
If the length of values is smaller than two then the list is sorted. Return values.
General case:
Calculate the middle point as len(values) // 2. Assign it to a variable named midpoint.
Use merge_sort() to sort the first half: values[:midpoint]. Assign the result to sorted_first_half.
Use merge_sort() to sort the second half: values[midpoint:]. Assign the result to sorted_second_half.
Use the merge_sorted_lists() function to return the result of merging sorted_first_half with sorted_second_half.
'''
def merge_sort(values):
    # Base case
    if len(values) < 2:
        return values
    # General case
    midpoint = len(values) // 2
    sorted_first_half = merge_sort(values[:midpoint])
    sorted_second_half = merge_sort(values[midpoint:])
    return merge_sorted_lists(sorted_first_half, sorted_second_half)

'''
A binary tree is a tree data structure in which each node has at most two children, 
referred to as the left child and the right child.
•We call the top node of the tree the "root."
•We call a node a "leaf" if it has no children.
•We call a node that is neither the root nor a leaf an "internal node."
•A binary search tree is a binary tree such that, for each node, all values 
on the left are smaller than or equal to the node value, and all values on the
right are larger than the node value.
•The height of a tree is the length of the longest path from the root to a leaf.
•The height of a binary tree is at most n - 1 and at least log2(n) where n is the number of nodes inthe tree.
'''

class Node:
    
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

'''
The rule that we'll follow is to have all values on the left be smaller than or equal to the value in the parent, 
and all values on the right bigger than the value parent value. This structure in known as a binary search tree.
The rule aplies to all nodes of the tree.
'''

class BST:
    
    def __init__(self):
        self.root = None
    '''
    The rule that we'll follow is to have all values on the left be smaller than or equal to the value in the parent, 
    and all values on the right bigger than the value parent value.

    Add is the method to be called be the user that uses recursion.
    '''    
    def add(self, value):
        if self.root is None:
            # The root does exist yet, create it
            self.root = Node(value)
        else:
            # Find the right place and insert new value
            self._add_recursive(self.root, value)
    '''
    If value is smaller than or equal to the value of current_node, then check whether the left child of current_node is None.
        If it is, create a new node with value, and assign it to the left child of current_node.
        Otherwise, call the add_recursive() method with the right child of current_node and value as arguments.
    If value is larger than the value of current_node, then check whether the right child of current_node is None.
        If it is, create a new node with value, and assign it to the right child of current_node.
        Otherwise, call the add_recursive() method with the right child of current_node and value as arguments.
    '''        
    def _add_recursive(self, current_node, value):
        if value <= current_node.value:
            # Go to the left
            if current_node.left_child is None:
                current_node.left_child = Node(value)
            else:
                self._add_recursive(current_node.left_child, value)
        else:
            # Go to the right
            if current_node.right_child is None:
                current_node.right_child = Node(value)
            else:
                self._add_recursive(current_node.right_child, value)
    '''
    If the current_node is None, then return False.
    Otherwise, compare value with the current_node value.
        If they are the same, return True.
        If the value is smaller, return the result of calling the same method but on the left child of current_node.
        If the value is bigger, return the result of calling the same method but on the right child of current_node.
    '''            
    def _contains(self, current_node, value):
        if current_node is None:
            return False
        if current_node.value == value:
            return True
        if value < current_node.value:
            return self._contains(current_node.left_child, value)
        return self._contains(current_node.right_child, value)
    '''
    Self and value reference that is used by end user to implement recursive _contains method 
    '''
    def contains(self, value):
        return self._contains(self.root, value)
'''
The conclusion is that, depending on the order in which the values are added to the tree, the complexity of the tree 
operations will range from linear complexity to logarithmic complexity. Linear complexity is not very good in this case 
since it is not better than a list. On the other hand, logarithmic complexity is much faster.
'''