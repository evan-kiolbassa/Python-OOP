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


'''
Extending the Node class with a new class named AVLNode. A node in an AVL tree needs the same information as a node in a 
BST plus two other values:
The height of the subtree rooted at that node.
The imbalance of that node.

In the initialization method of AVLNode, call the initialization method in Node to ensure that the self.value 
and self.children attributes are initialized using the super() function
'''
class AVLNode(Node):
    '''
    Inside the AVLNode class, define the __init__() method with two arguments:

    self: the self-reference that is automatically passed
    value: the value that the node will store
    Implement the __init__() method:

    Use the super() function to call the __init__() method from the Node class providing the value as argument.
    This initializes a parameter self.height to 1.
    This also initializes a parameter self.imbalance to 0
    '''
    def __init__(self, value):
        super().__init__(value)
        self.height = 1
        self.imbalance = 0
    
    '''
    Assign to a variable left_height the value of self.left_child.height if self.left_child isn't None. If it is None, then set it to 0.
    Assign to a variable right_height the value of self.right_child.height if self.right_child isn't None. If it is None, then set it to 0.
    Set the self.height value to be 1 plus the maximum between left_height and right_height.
    Set the self.imbalance value to be the difference left_height and right_height.
    '''    
    def calculate_height_and_imbalance(self):
        # Calculate left height
        left_height = 0
        if self.left_child is not None:
            left_height = self.left_child.height
        # Calculate right height
        right_height = 0
        if self.right_child is not None:
            right_height = self.right_child.height
        # Use formulas to calculate height and imbalance
        self.height = 1 + max(left_height, right_height)
        self.imbalance = left_height - right_height

class AVLTree(BST):
    
    def __init__(self):
        super().__init__()
        
    def _add_recursive(self, current_node, value):
        if current_node is None:
            return AVLNode(value)
        if value <= current_node.value:
            current_node.left_child = self._add_recursive(current_node.left_child, value)
        else:
            current_node.right_child = self._add_recursive(current_node.right_child, value)
        current_node.calculate_height_and_imbalance() 
        # Update the height and imbalance for current_node by calling the AVLNode.calculate_height_and_imbalance() method
        if abs(current_node.imbalance) == 2:
            return self._balance(current_node)
        return current_node
        
    def get_height(self):
        return self.root.height
    
    '''
    The strategy of AVL trees to maintain a low height is to keep the imbalance factors of all nodes low. 
    This means that for any given node, its imbalance is either -1, 0 or 1. As soon as a node 
    reaches an imbalance value of -2 or 2, an operation called a "tree rotation" is applied to restore the 
    balance in the tree.
    '''

    '''
    Assign the right child of node to a variable named pivot.
    Set the right child of node to be the left child of pivot.
    Set the left child of pivot to be node.
    Update the height and imbalance of the node by calling the AVLNode.calculate_height_and_imbalance().
    Update the height and imbalance of the pivot by calling the AVLNode.calculate_height_and_imbalance().
    Return the pivot node. We will use this return value later.
    '''
    def _rotate_left(self, node):
        pivot = node.right_child
        node.right_child = pivot.left_child
        pivot.left_child = node
        node.calculate_height_and_imbalance()
        pivot.calculate_height_and_imbalance()
        return pivot
    
    '''
    Assign the left child of node to a variable named pivot.
    Set the left child of node to be the right child of pivot.
    Set the right child of pivot to be node.
    Update the height and imbalance of the node by calling the AVLNode.calculate_height_and_imbalance().
    Update the height and imbalance of the pivot by calling the AVLNode.calculate_height_and_imbalance().
    Return the pivot node. We will use this return value later.
    '''

    def _rotate_right(self, node):
        pivot = node.left_child
        node.left_child = pivot.right_child
        pivot.right_child = node
        node.calculate_height_and_imbalance()
        pivot.calculate_height_and_imbalance()
        return pivot
    
    '''
    Write an if statement to check whether the node imbalance equals 2.
    Inside the if statement, assign the node.left_child to a variable named pivot.
    If the imbalance of the pivot is equal to 1, return the result of rotating node to the right.
    '''

    def _balance(self, node):
        if node.imbalance == 2:
            pivot = node.left_child
            if pivot.imbalance == 1:
                return self._rotate_right(node)
            else:
                node.left_child = self._rotate_left(pivot)
                return self._rotate_right(node)
        else:
            pivot = node.right_child
            if pivot.imbalance == -1:
                return self._rotate_left(node)
            else:
                node.right_child = self._rotate_right(pivot)
                return self._rotate_left(node)

# Test height with sequential inserts, the height should be much smaller than NUM_VALUES
NUM_VALUES = 10000
avl = AVLTree()
for i in range(NUM_VALUES):
    avl.add(i)
print(avl.root.height)

# Test height with random inserts, the height should be much smaller than NUM_VALUES
import random
random.seed(0)
rnd_values = [random.randint(1, 1000000) for _ in range(NUM_VALUES)]
avl = AVLTree()
for v in rnd_values:
    avl.add(v)
print(avl.root.height)

# Test contains method
for v in rnd_values:
    assert avl.contains(v)

# Compare runtime with list, AVL should be faster
import time
times_list = []
times_avl = []

for v in rnd_values:
    start = time.time()
    v in rnd_values
    end = time.time()
    times_list.append(end - start)
    
    start = time.time()
    avl.contains(v)
    end = time.time()
    times_avl.append(end - start)
    
import matplotlib.pyplot as plt
plt.plot(times_list, label="list")
plt.plot(times_avl, label="AVL")
plt.legend()

'''
A heap is a binary tree in which every level except for the last one is full.
•A min-heap is a heap where the value of each node is smaller than or equal to 
the value of itschildren.
•A binary tree is complete if the tree's levels are filled in except for the last,
 which has nodes filledin from left to right.
 •Heaps have many applications. In data engineering, we can use them to schedule tasks 
 with priorities. In data science, we can use them to calculate order statistics on the data. T
 hey have many applications, including calculating the shortest routes in your GPS.
 •The time complexity of heap operations is logarithmic in the worst case. This makes 
 a heap very efficient data structure when we need to keep track of minimums (or maximums for a max-heap)
'''

class MinHeap:
    '''
    initializes an empty list and stores it in self.values.
    '''
    def __init__(self):
        self.values = []
    '''
    Define a method named _left_child() with two arguments:
    self: the self-reference
    node: the index of the node for which we want to get the left child
    Implement the _left_child() method so that it uses the above formula 
    to calculate and return the index of the left child of the node with index node.
    '''
    def _left_child(self, node):
        return 2 * node + 1
    '''
    Define a method named _right_child() with two arguments:
    self: the self-reference
    node: the index of the node for which we want to get the right child
    Implement the _right_child() method so that it uses the above formula 
    to calculate and return the index of the right child of the node with index node.
    '''
    def _right_child(self, node):
        return 2 * node + 2
    '''
    Returns the parent index of a given node.
    '''
    def _parent(self, node):
        return (node - 1) // 2

    '''
    Given two node indexes, swaps their values in the list.
    '''
    def _swap(self, node1, node2):
        tmp = self.values[node1]
        self.values[node1] = self.values[node2]
        self.values[node2] = tmp
    '''
    An add() method that will append the new value to the end 
    of the values list and call the _heapify_up() method to 
    restore the min-heap order property.
    '''
    def add(self, value):
        self.values.append(value)
        self._heapify_up(len(self.values) - 1)
    '''
    Use the MinHeap._parent() method to calculate the index of the parent of node. Assign the result to parent.
    Check whether node is not the root and whether the value of the parent is larger than the value of node. If both conditions are true, we need to fix the order by doing the following:
    Use the MinHeap._swap() method to swap node and parent
    Call _heapify_up() on parent to recursively go up the tree and continue fixing it.
    '''
    def _heapify_up(self, node):
        parent = self._parent(node)
        if node > 0 and self.values[parent] > self.values[node]:
            self._swap(node, parent)
            self._heapify_up(parent)

    '''
    Returns the minimum value 
    '''       
    def min_value(self):
        return self.values[0]
    
    def pop(self):
        self._swap(0, len(self.values) - 1)
        ret_value = self.values.pop()
        self._heapify_down(0)
        return ret_value
    '''
    Store the current root value (minimum) in a variable.
    Swap the root with the last node.
    Remove the last element from the list.
    Heapify down to fix the order properties.

    Calculate the left and right children indexes. Assign them to left_child and right_child, respectively.
    By inspecting the self.values attribute, determine whether left_child or right_child has the smaller value. 
    Assign it to min_node. Be aware of the cases where one or both children do not exist.
    If min_node exists, do the following:
        Swap the value of node with the values of min_node.
        Recursively call the _heapify_down() method on min_node to continue fixing down the tree.
    '''
    def _heapify_down(self, node):
        left_child = self._left_child(node)
        right_child = self._right_child(node)
        min_node = node
        if left_child < len(self.values) and self.values[left_child] < self.values[node]:
            min_node = left_child
        if right_child < len(self.values) and self.values[right_child] < self.values[min_node]:
            min_node = right_child
        if min_node != node:
            self._swap(node, min_node)
            self._heapify_down(min_node)

'''
A B-tree is a special type of search tree in which nodes can have more than two children.
•We can use the binary search algorithm to insert an entry into a node while preserving its 
sorted property in the keys. This is more efficient than inserting the entry and then sorting the list.
•The bisect Python module provides an implementation of the binary search algorithm. It can find in O(log(n)) 
the correct index of the insertion of a key in a sorted list.
•Nodes in B-tree keep several entries. Special split operations allow us to split the nodes into two nodes with 
the objective of keeping the maximum number of entries in any given node below agiven threshold. 
This, in turn, keeps the insertion of entries inside nodes a constant time operation, O(1)
'''
import bisect
class BNode:
    '''
    If keys isn't None, then it stores the provided keys list in self.keys. Otherwise, it stores an empty list [] into self.keys.
    If values isn't None, then it stores the provided values list in self.values. Otherwise, it stores an empty list [] into self.values.
    '''
    def __init__(self, keys=None, values=None, children=None, parent=None):
        self.keys = keys or []
        self.values = values or []
        self.parent = parent
        self.set_children(children) 
    '''
    Stores the provided children list into self.children if children isn't None. If it is None, then initialize self.children as an empty 
    list [].
    '''    
    def set_children(self, children): 
        self.children = children or []
        for child in self.children:
            child.parent = self
    # Returns the length of the node list
    def __len__(self):
        return len(self.values)
    # Return True if the node is a leaf (has no children) and False otherwise.
    def is_leaf(self):
        return len(self.children) == 0
    # Returns True if self.keys contains key and False otherwise.
    def contains_key(self, key):
        return key in self.keys
    # returns the value associated with the provided key.
    # If the key doesn't exist in the node, return None instead.
    def get_value(self, key):
        for i, k in enumerate(self.keys):
            if k == key:
                return self.values[i]
        return None
    # Use the bisect.bisect() function to calculate the index of self.keys where the given key should be inserted.
    # Return that index.
    def get_insert_index(self, key):
        return bisect.bisect(self.keys, key)
    '''
    Use the get_insert_index() method to calculate the insert index of key in self.keys. Assign the result to a variable named insert_index.
    Use the list.insert method to insert key into self.keys at index index.
    Use the list.insert method to insert value into self.values at index index.
    Add a return statement at the end of the insert_entry() method so that it returns index.
    '''
    def insert_entry(self, key, value):
        insert_index = self.get_insert_index(key)
        self.keys.insert(insert_index, key)
        self.values.insert(insert_index, value)
        return insert_index
    '''
    Calculate the split index by dividing the length of the current node by two. Assign it to a variable split_index.

    Store the element of self.keys at index split_index into a variable named key_to_move up.

    Store the element of self.values at index split_index into a variable named value_to_move up.

    Create a node called right_node by providing the second half of the values and children of the current node:

        The keys should be self.keys[split_index+1:].
        The values should be self.values[split_index+1:].
        The children should be self.children[split_index+1:].
        Update the current node by removing the second half of the values and children:

    Set self.keys to self.keys[:split_index].
    Set self.values to self.values[:split_index].
    Set self.children to self.children[:split_index+1].
    Create the parent node as follows:

        The keys should be a singleton list [key_to_move_up].
        The values should be a singleton list [value_to_move_up].
        The children should list [self, right_node].
    Return the parent node.
    '''
    def split_no_parent(self):
        split_index = len(self) // 2
        key_to_move_up = self.keys[split_index]
        value_to_move_up = self.values[split_index]
        right_node = BNode(self.keys[split_index+1:], self.values[split_index+1:], self.children[split_index+1:])
        self.keys = self.keys[:split_index]
        self.values = self.values[:split_index]
        self.children = self.children[:split_index+1]
        parent = BNode([key_to_move_up], [value_to_move_up], [self, right_node])
        return parent
    '''
    self: the self-reference
    insert_index: the index of self.children where we want to insert the child
    child: the child node that we want to insert
    Implement the insert_child() method using the list.insert() method to insert the given child at the given insert_index in self.children.

    Update the parent of child to self.
    '''
    def insert_child(self, insert_index, child):
        self.children.insert(insert_index, child)
        child.parent = self
    '''
    Define a method named split_with_parent() with only the self argument. Implement according to the following instructions.

    Calculate the split index by dividing the length of the current node by two. Assign it to a variable split_index.

    Store the key at that index in a variable named key_to_move_up.

    Store the value at that index in a variable named value_to_move_up.

    Create a node called right_node by providing the second half of the values and children of the current node:

        The keys should be self.keys[split_index+1:].
        The values should be self.values[split_index+1:].
        The children should be self.children[split_index+1:].
    
    Remove the second half of the values in the current node:

        Set self.keys to self.keys[:split_index].
        Set self.values to self.values[:split_index].
        Set self.children to self.children[:split_index+1].
        
    Use the insert_entry() method to insert key_to_move_up 
    and value_to_move_up into self.parent. Assign the index where the entry was inserted to a variable named insert_index.

    Use the insert_child() method to insert the right_node as a child of self.parent.
     The insertion index should be equal to insert_index + 1.

    Return the self.parent node.
    '''    
    def split_with_parent(self): 
        split_index = len(self) // 2
        key_to_move_up = self.keys[split_index]
        value_to_move_up = self.values[split_index]
        right_node = BNode(self.keys[split_index+1:], self.values[split_index+1:], self.children[split_index+1:])
        self.keys = self.keys[:split_index]
        self.values = self.values[:split_index]
        self.children = self.children[:split_index+1]
        insert_index = self.parent.insert_entry(key_to_move_up, value_to_move_up)
        self.parent.insert_child(insert_index + 1, right_node)
        return self.parent
    '''
    Define a method named split() with only the self argument.

    Implement the split() method by using an if statement to check whether self.parent is None.

    If it's None, return the result of calling self.split_no_parent()
    Otherwise, return the result of calling self.split_with_parent().
    '''
    def split(self): # Instruction 1
        if self.parent is None: # Instruction 2
            return self.split_no_parent()
        return self.split_with_parent()

'''
A B-tree is an ordered dictionary. It is less efficient than a plain dictionary, but the order can 
be leveraged to perform other types of queries.•B-tree operations have logarithmic time complexities 
O(log(N)) where N is the number of entries.
'''
class BTree:
    '''
    Implement the __init__() method so that it does the following:
    Specifies a split threshold
    Creates an empty Node and stores in into self.root
    Initializes the tree height by setting self.height to 0
    Initializes the tree size by setting self.size to 0
    '''
    def __init__(self, split_threshold):
        self.split_threshold = split_threshold
        self.root = Node()
        self.height = 0
        self.size = 0

    def __len__(self):
        return self.size
    '''
    Define a method named find_node() method with three arguments:

    self: the self-reference
    current_node: the current node where we are searching
    key: the key that we are searching for
    Implement the base case of the find_node() method by doing the following:

    Use the Node.contains_key() method with key as argument to check whether the 
    current_node contains the provided key. If it does, return current_node.
    Use the Node_is_leaf() method to check whether the current_node is a leaf. If it is, return None.
    Implement the general case of the find_node() method by doing the following:

    Using the Node.get_insert_index() method to calculate the index of the child of current_node where 
    we need to continue searching. Assign the result to child_index.
    Return the result of calling the find_node() method using the child of current_node with index 
    child_index as the new node. The key remains the same.
    '''
    def _find_node(self, current_node, key):
        if current_node.contains_key(key):
            return current_node
        if current_node.is_leaf():
            return None
        child_index = current_node.get_insert_index(key) 
        return self._find_node(current_node.children[child_index], key)
    '''
    Returns whether or not the given key is stored in the B-tree. You can 
    do this by calling self._find_node() on self.root and checking to see 
    if the result isn't None.
    '''
    def contains(self, key):
        node = self._find_node(self.root, key)
        return not node is None
    '''
    Use the _find_node() method with self.root and key to find whether the node exists. Assign the result to a variable named node.
    If the node is None, return None.
    If the node isn't None, use the Node.get_value() method with key as argument to get the value associated to the provided key.
    '''
    def get_value(self, key):
        node = self._find_node(self.root, key)
        if node is None:
            return None
        return node.get_value(key)
    '''
    Define a method named add() method with four arguments:

        self: the self-reference
        current_node: the current node where we are searching
        key: the key that we want to insert
        value: the value associated with the key
    Implement the base case of the add() method. If the current_node is a leaf, do the following:

        Use the Node.insert_entry() method with arguments key and value to insert the entry inside the current_node.
    
    Implement the general case of the add() method. Else, if the current_node isn't a leaf, then do the following:

        Use the Node.get_insert_index() method with key as argument to calculate the index of the child of current_node where we need to continue searching. Assign the result to child_index.
        Call the add() method on the child with index child_index. The key and value remain the same.
    '''
    def _add(self, current_node, key, value):
        if current_node.is_leaf(): 
            current_node.insert_entry(key, value)
        else:
            child_index = current_node.get_insert_index(key)
            self._add(current_node.children[child_index], key, value)
        if len(current_node) > self.split_threshold:
            parent = current_node.split()
            if current_node == self.root:
                self.root = parent
                # Increment height here
                self.height += 1 # Instruction 1
    '''
    Calls self._add() with the tree root, the provided key, and value as arguments.
    Increments the value of self.size
    '''
    def add(self, key, value):
        self._add(self.root, key, value)
        self.size += 1


bt = BTree(2) 
heights = []
for i in range(1, 1001): 
    bt.add(i, i) 
    heights.append(bt.height) 
plot(heights)