'''
Linked list data structures are advantageous in cases where stored data does
not need to be accessed by index. Operations run in constant time.
Linked lists are implemented by linking nodes.  
'''


'''
A list such as [5, 3, 8] will be stored as 3 separate objects in a linked structure. Each of these objects will store the 
value plus references (links) to the neighboring elements. To build a linked structure, we use an auxiliary class that is 
commonly called a node. The node keeps track of three things: The data, the previous node, and the next node
'''

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

'''
The linked list will be implemented in a class named LinkedList. This class will use the Node class to chain the data together into 
a list-like structure. The first node of a linked list is commonly known as head while the last node of a list is called the tail.
Linkedlist object will keep track of list length, head node, and tail node
'''
    
    class LinkedList:
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0
    '''
    Append method for the LinkedList class. If the list is empty, the head and tail are equal to the new node
    if not empty, then the next tail is equal to new data point and the previous tail is documented. 
    '''   
    def append(self, data):
        new_node = Node(data)
        if self.length == 0:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1
    '''
    Iter method allows for the class object to be iterable. The __iter__ method should always return self for a reference to the object
    that is being iterated over. _iter_node is an attribute that keeps track of the current node. The "_" notation in front of the attribute
    denotes that the attribute is internal and not accessible to the end user. 
    '''    
    def __iter__(self):
        self._iter_node = self.head
        return self 
    '''
    Returns the current iteration value stored at _iter_node. 
    Moves _iter_node to the next value.
    Stops when the iteration is over (When _iter_node is equal to None)
    '''
    def __next__(self):
        if self._iter_node is None:
            raise StopIteration
        ret = self._iter_node.data
        self._iter_node = self._iter_node.next
        return ret
    '''
    Prepending data involves adding data to the head of the list
    Set the previous node of the current head to the newly created node.
    Set the next node of the newly created node to be the current head.
    Making the newly created node become the new head.
    '''
    def prepend(self, data):
        new_node = Node(data)
        if self.length == 0:
            self.head = self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node
        self.length += 1
    '''
    Allows for the use of the built-in length function in the LinkedList class
    '''   
    def __len__(self):
        return self.length
    '''
    Uses list comprehension to convert the values in the LinkedList class into a standard
    Python list and surround the list on quotes
    '''
    def __str__(self):
        return str([value for value in self])


'''
Queues are a first-in, first-out (FIFO) data structure. This means that they work like a supermarket queue 
where the first client to be served is the first to arrive in the queue.
•Queues can be implemented by extending the linked list data structure. 
When we extend a classin Python all the attributes and methods are automatically available to the new class.
•Inheritance (class extension) is a very powerful programming tool because it allows transferfunctionality from 
one class to another. It promotes code re-usability.
•The FCFS scheduling algorithm is an algorithm for scheduling usage of a single shared resource.Usage is granted 
in a first-come, first-served fashion.•The wait time of a process is the time between when the process arrives and the time it 
starts being executed.
•The turnaround time of a process is the time between when the process arrives and the time it terminates
'''
class Queue(LinkedList):
    '''
    The enqueue method utilizes the prepend method from the LinkedList class.
    Enqueue means to add an element to the front of the list
    '''
    def enqueue(self, data):
        self.prepend(data)
    '''
    Acquires the data attribute of the tail node, the front of the queue
    '''    
    def get_front(self):
        return self.tail.data
    
    '''
    Method that removes the front of the queue. 
    Store the data attribute of the tail in a variable so we can return it in the end.
    Update the tail to become the previous node of the current tail (move the tail back one position).
    Set the next element of the new tail to be None
    Subtract 1 from the list length
    '''
    def dequeue(self):
        ret = self.tail.data
        if self.length == 1:
            self.tail = self.head = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.length -= 1
        return ret

cur_time = 0
num_processes_done = 0
wait_queue = Queue()
cur_pid = None

# Process dataframe columns are ['Pid', 'Arrival', 'Duration', 'Start', 'End']
# The Pid column represents the process identifiers. The Arrival column represents the time 
# at which the processor received the task. Finally, the Duration column gives the time the task required to run.
'''
While loop condition is terminated once the number of completed processes is equal to 
the number of rows in the process dataframe
'''
while num_processes_done < processes.shape[0]:
    # Check if current process finished
    if cur_pid is not None:
        if processes.loc[cur_pid, "Start"] + processes.loc[cur_pid, "Duration"] == cur_time:
            '''
            Handle end of the process: If cur_pid is not None, then we check whether its starting time 
            plus its duration are equal to cur_time. If they are, it means the process is done executing. 
            We can then set the end time of this process to cur_time and set cur_pid to None to free the processor.
            '''
            processes.loc[cur_pid, "End"] = cur_time
            cur_pid = None
            num_processes_done += 1
    # Handle arriving processes
    '''
    Find all processes with arrival time equal to cur_time and add them to the wait_queue.
    '''
    ready_processes = processes[processes["Arrival"] == cur_time]
    for pid, _ in ready_processes.iterrows():
        wait_queue.enqueue(pid)
    # Assign a process to the processor
    if cur_pid is None and len(wait_queue) > 0:
        '''
        If the processor is free, that is, cur_pid is None, and there are processes waiting in the queue then 
        remove the process at the front of the queue and assign it to cur_pid. 
        We also need to set its start time to cur_time
        '''
        cur_pid = wait_queue.dequeue()
        processes.loc[cur_pid, "Start"] = cur_time 
    cur_time += 1
    
print(processes.head())

processes["Wait"] = processes["Start"] - processes["Arrival"]
average_wait_time = processes["Wait"].mean()

processes["Turnaround"] = processes["End"] - processes["Arrival"]
average_turnaround_time = processes["Turnaround"].mean()



# Stacks are a last-in, first-out (LIFO) data structure. 
# The LCFS scheduling algorithm is an algorithm for scheduling 
# usage of a single shared resource.Usage is granted in a last-come, first-served fashion. 
# It can have advantages in situations wherethe age of processes is related to their urgency
class Stack(LinkedList):
    '''
    The push method method assigns values to the top of the stack by using
    the apen method defined in the LinkedList class
    '''
    def push(self, data):
        self.append(data)
    # peek method returns the top element without deleting it
    def peek(self):
        return self.tail.data
    # pop method removes and retrieves the top part of the stack.
    '''
    Store the data attribute of the tail in a variable so we can return it in the end.
    Update the tail to the previous node of the current tail (move the tail back one position).
    Set the next element of the new tail to be None.
    '''
    def pop(self):
        ret = self.tail.data
        if self.length == 1:
            self.tail = self.head = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.length -= 1
        return ret
'''
The Pid column represents the process identifiers. 
The Arrival column represents the time at which the processor received the task. 
Finally, the Duration column gives the time the task required to run.
'''

cur_time = 0
num_processes_done = 0
wait_stack = Stack()
cur_pid = None


while num_processes_done < processes.shape[0]:
    # If cur_pid is not None, then we check whether its starting time plus its duration are equal to cur_time. 
    # If they are, it means the process is done executing. We can then set the end time of this process to cur_time 
    # and set cur_pid to None to free the processor.
    if cur_pid is not None:
        if processes.loc[cur_pid, "Start"] + processes.loc[cur_pid, "Duration"] == cur_time:
            processes.loc[cur_pid, "End"] = cur_time
            cur_pid = None
            num_processes_done += 1
    # Find all processes with arrival time equal to cur_time and add them to the wait_stack.
    ready_processes = processes[processes["Arrival"] == cur_time]
    for pid, _ in ready_processes.iterrows():
        wait_stack.push(pid)
    # If the processor is free, that is, cur_pid is None, and there are processes waiting in the stack then remove the 
    # process at the top of the stack and assign it to cur_pid. We also need to set its start time to cur_time.
    if cur_pid is None and len(wait_stack) > 0:
        cur_pid = wait_stack.pop()
        processes.loc[cur_pid, "Start"] = cur_time 
    cur_time += 1

processes["Wait"] = processes["Start"] - processes["Arrival"]
average_wait_time = processes["Wait"].mean()

fcfs_max_wait = processes["FCFS Wait"].max()
lcfs_max_wait = processes["Wait"].max()

processes["Turnaround"] = processes["End"] - processes["Arrival"]
average_turnaround_time = processes["Turnaround"].mean()



'''
Dictionaries work by mapping keys into a range of integers 0 to B - 1. 
The entries are stored byallocating an array-like data structure with B entries.
•To calculate the bucket index of a key we use a hash function to convert the key 
to an integerand then a compression function to reduce that integer to the range 0 to B - 1.
•A common compression function is h % B where h is the hash code of the key.
•A collision occurs when two keys map to the same bucket. One way to handle collisions is to 
use a linked list to store all entries that map to a given bucket index. 
This technique is called separate chaining.•The time complexity of dictionary operations is O(N) 
in the worst case. However, if we use goodhash functions and a good number of buckets the complexity 
is expected to be O(1) instead.•The dictionary efficiency strongly depends on the load factor N / B. 
A good rule of thumb is tomaintain the load factor below 0.75. This can be done by increasing B when N increases.
•We need to be careful when selecting or increasing B. A good rule of thumb is to use a primenumber for the value of B


It is assumed that keys are integers and use a compression function to squeeze the keys into the range 0 to B - 1, 
where B is the number of buckets (length of the list).
However, some keys must be mapped to the same bucket index because there are infinitely many possible keys and only 
a finite number of buckets. This is called a "collision". "Separate chaining" can be used to overcome this. 
Separate chaining consists of using a list to store the elements in each bucket. Because the list elements do not
need to be accessed by index, linked list will provide superior performance.
'''

class Dictionary:
    
    def __init__(self, num_buckets):
        # Initializes a linked list instance for each bucket
        self.num_buckets = num_buckets
        self.buckets = [LinkedList() for _ in range(num_buckets)]
        self.length = 0
    # The process of transforming an object into an integer is called hashing. 
    # The transformation function is called a hash function and the result it called hash code
    # For example, you can convert a string into hash code
    # Keys should be immutable objects (ie strings or tuples that cannot be modified)
    # The _get_index method returns the bucket number using the % operator
    def _get_index(self, key):
        hashcode = hash(key)
        return hashcode % self.num_buckets
    '''
    Use the _get_index() method to calculate the index of the bucket for the provided key. Assign it to a variable named index.
    Declare a boolean value named found_key initially set to False.
    Use a for loop to iterate over all entries in self.buckets[index] using a variable named entry. For each entry, check whether entry 
    key is equal to key. If it is, update entry.value to value and set found_key to True.
    '''   
    def put(self, key, value):
        index = self._get_index(key)
        found_key = False
        for entry in self.buckets[index]:
            if entry.key == key:
                entry.value = value
                found_key = True
        '''
        After the for loop, check whether found_key is False. If it is:
        Use the Entry() constructor to create a new entry with the provided key and value.
        Append the new entry to self.buckets[index].
        Update the length of the dictionary by incrementing self.length.
        '''
        if not found_key:
            self.buckets[index].append(Entry(key, value))
            self.length += 1
    '''
    Use the _get_index() method to calculate the index of the bucket for the provided key. Assign it to a variable named index.
    Use a for loop to iterate over all entries in self.buckets[index] using a variable named entry. For each entry, check whether 
    entry.key is equal to key. If it is, return entry.value.
    '''       
    def get_value(self, key):
        index = self._get_index(key)
        for entry in self.buckets[index]:
            if entry.key == key:
                return entry.value
        '''
        After the for loop, raise a KeyError with argument key. Note that because of the return statement inside the for loop, 
        this line of code is only executed if no matching key is found.
        '''
        raise KeyError(key)
    '''
    Calculate the bucket index of the given key.
    Create an empty linked list.
    Iterate over all entries in that bucket and append to the new linked list all entries whose key is different from the key 
    that we want to delete.
    Update the length of the dictionary. We need to decrement it if the new list has fewer elements than the original bucket.
    We replace the list from the bucket with the new list.
    '''
    def delete(self, key):
        index = self._get_index(key)
        new_bucket = LinkedList()
        for entry in self.buckets[index]:
            if entry.key != key:
                new_bucket.append(entry)
        if len(new_bucket) < len(self.buckets[index]):
            self.length -= 1
        self.buckets[index] = new_bucket
    '''
    When we use the bracket notation d["my key"], Python tries to call the __getitem__() 
    method by providing "my key" as argument. Therefore, to make this work, we can implement 
    the __getitem__() method by calling the already existing get_value() method
    '''
    def __getitem__(self, key):
        return self.get_value(key)
    '''
    Similarly, when we write d["my key"] = 1, Python tries to call the __setitem__() method with 
    arguments "my key" and 1. In the same way, to make it work, we can implement the __setitem__() 
    method by calling the already existing put() method
    '''
    def __setitem__(self, key, value):
        self.put(key, value)
    '''
    Another improvement we are going to add is the __len__() method so that we enable using the len() 
    built-in function on the Dictionary class.
    '''
    def __len__(self):
        return self.length

