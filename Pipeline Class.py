import csv
import itertools
'''
File streaming works by breaking a file into small sections, and then loaded one at a time intomemory.
•A generator is an iterable object that is created from a generator function.
•A generator differs from a regular function in two important ways:•A generator uses yield instead of return.
•Local variables are kept in memory until the generator completes.
The yield expression:•Lets the Python interpreter know that the function is a generator.
•Suspends the function execution, keeping the local variables in memory until the next call.
•Once the final yield in the generator is executed, the generator will have exhausted all of itselements.
'''
def parse_log(log):
    for line in log:
        split_line = line.split()
        remote_addr = split_line[0]
        time_local = split_line[3] + " " + split_line[4]
        request_type = split_line[5]
        request_path = split_line[6]
        status = split_line[8]
        body_bytes_sent = split_line[9]
        http_referrer = split_line[10]
        http_user_agent = " ".join(split_line[11:])
        yield (
            remote_addr, time_local, request_type, request_path,
            status, body_bytes_sent, http_referrer, http_user_agent
        )
first_line = next(parse_log(log))

def build_csv(lines, file, header=None):
    if header:
        lines = itertools.chain([header], lines)
    writer = csv.writer(file, delimiter=',')
    writer.writerows(lines)
    file.seek(0)
    return file

file = open('temporary.csv', 'r+')
csv_file = build_csv(
    parsed,
    file,
    header=[
        'ip', 'time_local', 'request_type',
        'request_path', 'status', 'bytes_sent',
        'http_referrer', 'http_user_agent'
    ]
)

def count_unique_request(csv_file):
    reader = csv.reader(csv_file)
    header = next(reader)
    idx = header.index('request_type')
    
    uniques = {}
    for line in reader:
        
        if not uniques.get(line[idx]):
            uniques[line[idx]] = 0
        uniques[line[idx]] += 1
    return ((k, v) for k,v in uniques.items())



log = open('example_log.txt')
parsed = parse_log(log)
file = open('temporary.csv', 'r+')
csv_file = build_csv(
    parsed,
    file,
    header=[
        'ip', 'time_local', 'request_type',
        'request_path', 'status', 'bytes_sent',
        'http_referrer', 'http_user_agent'
    ]
)

uniques = count_unique_request(csv_file)
summarized_file = open('summarized.csv', 'r+')
summarized_csv = build_csv(uniques, summarized_file, header=['request_type', 'count'])
print(summarized_file.readlines())

import io
'''
Logger function logs when function calls are made to
improve debugging capabilities of production code. 
This function can be applied using decorator syntax, "@",
which allows a function to be wrapped by another function.
'''
def logger(func):
    def inner(*args):
        print('Calling function: {}'.format(func.__name__))
        print('With args: {}'.format(args))
        return func(*args)
    return inner
'''
Tries to run and return a given function.
If any exception is thrown, catches the exception, and returns the exception object.

Uses catch_error decorator syntax to wrap throws_error function.
'''
def catch_error(func):
    def inner(*args):
        try:
            return func(*args)
        except Exception as e:
            return e
    return inner

@catch_error
def throws_error():
    raise Exception('Throws Error')

'''
We want the tasks to come in an ordered format. This ordering is based on the execution of our tasks, 
where we want the pipeline to run starting from the first_task() function, then executing the second_task(). 
The depends_on keyword argument enforces this ordering, so we can determine the dependency link of each task.
'''
class Pipeline:
    def __init__(self):
        self.tasks = []
        
    def task(self, depends_on=None):
        idx = 0
        if depends_on:
            # If depends_on condition is true, the next task is the
            # previous index + 1
            idx = self.tasks.index(depends_on) + 1
        def inner(f):
            # Inser the passed function into the desired index
            # of the task list
            self.tasks.insert(idx, f)
            return f
        return inner
    '''
    The run() method takes in an input_ argument.
    Then, iterates through the self.tasks property, and call each function with the previous output.
    '''
    def run(self, input_):
        output = input_
        for task in self.tasks:
            output = task(output)
        return output
    
pipeline = Pipeline()

# Wrapping functions with pipeline task method to assign run dependencies
@pipeline.task()
def parse_logs(logs):
    return parse_logs(logs)

@pipeline.task(depends_on=parse_logs)
def build_raw_csv(lines):
    return build_csv(lines, header=[
        'ip', 'time_local', 'request_type',
        'request_path', 'status', 'bytes_sent',
        'http_referrer', 'http_user_agent'
    ],
    # The StringIO object mimicks a file-like object that, instead of writing out to disk, 
    # keeps a file-like object in memory.
    file=io.StringIO())

@pipeline.task(depends_on=build_raw_csv)
def count_uniques(csv_file):
    return count_unique_request(csv_file)

@pipeline.task(depends_on=count_uniques)
def summarize_csv(lines):
    return build_csv(lines, header=['request_type', 'count'], file=io.StringIO())

print(pipeline.tasks)

log = open('example_log.txt')
summarized_file = pipeline.run(log)
print(summarized_file.readlines())

# Check val
"['request_type,count\r\n', 'GET,3334\r\n', 'POST,3299\r\n', 'PUT,3367\r\n']"

'''
Above pipeline implementation is not suitable for most cases due to
the linearity of the task scheduling. 

Directed acyclic graphs (DAG) allow the creation of a branched pipeline 
data structure for enhanced task scheduling

Graph: The data structure is composed of vertices (nodes) and edges (branches).
Directed: Each edge of a vertex points only in one direction.
Acyclic: The graph does not have any cycles.

DAG structure naturally creates an efficient ordering of dependent tasks. 
Implementation of task scheduling in linear time, 
O(V + E), where V and E are number of vertces and edges.

The use case for the DAG is to place tasks in an order of dependencies. 
The ideal ordering of tasks is to begin with the task with highest dependency
and end with the least depended on. In this pipeline example, it is ideal
to start with parsing a file, and ending with summarizing.

To find a longest path, it's necessary to know which nodes "start" the directed graph. 
meaning the root nodes that the graph expands from. Root nodes contain zero in-degrees
which is what distinguishes root nodes from non-root nodes.

The number of in-degrees is the total count of edges pointing towards the node.
'''

from collections import deque

class DAG:

    def __init__(self):
        self.graph = {}
    '''
    Add node to self.graph if it isn't already in the graph and default the value to a list.
    If there is a to, add that to the node's list, and add to self.graph defaulting to a list
    '''
    def add(self, node, to=None):
        def add(self, node, to=None):
        if not node in self.graph:
            self.graph[node] = []
        if to:
            if not to in self.graph:
                self.graph[to] = []
            self.graph[node].append(to)
    # The in_degrees() method should create DAG.degrees attribute containing a dictionary mapping of node to number of in-degrees.
    # Loop through every node, and its pointers, and then count each edge to the pointed node.
    def in_degrees(self):
        self.degrees = {}
        for node in self.graph:
            if node not in self.degrees:
                self.degrees[node] = 0
            for pointed in self.graph[node]:
                if pointed not in self.degrees:
                    self.degrees[pointed] = 0
                self.degrees[pointed] += 1
    
    '''
    Filter all the root nodes, and pop them off the graph.
    Search their pointers, and check if they are the new root nodes.
        If one is, append it to the root nodes list, and pop it off the graph.
        If not, then continue.
    Once all the nodes have been popped from the graph, return the list of ordered root nodes.
    '''
    def sort(self):
        self.in_degrees()
        to_visit = deque()
        for node in self.graph:
            if self.degrees[node] == 0:
                to_visit.append(node)
        '''
        Using in_degrees, place the root node(s) in a queue.
        While the queue is not empty:
            Deque a node, node_i.
            Check each of the pointers in the node.
            Decrement the pointer's in_degrees by 1 (reduce pointers).
            If that pointer's # of in-degrees is 0, add it to the queue.
            If not, continue.
            Once all the pointers have been searched, append node_i to the list searched.
            Continue the while loop.
        Return the searched list.
        '''
        searched = []
        while to_visit:
            node = to_visit.popleft()
            for pointer in self.graph[node]:
                self.degrees[pointer] -= 1
                if self.degrees[pointer] == 0:
                    to_visit.append(pointer)
            searched.append(node)
        return searched
    '''
    Call sort() in the add() method, and check if the sorted length is greater than the number of nodes in the graph.
    Raise Exception if a cycle is detected.
    '''

    def cycle_check(self):
        if len(self.sort()) != len(self.graph):
                raise Exception

    @cycle_check()           
    def add(self, node, to=None):
        return add(self, node, to=None)



class Pipeline():
    def __init__(self):
        self.tasks = DAG()
        
    def task(self, depends_on=None):
        def inner(f):
            self.tasks.add(f)
            if depends_on:
                self.tasks.add(depends_on, f)
            return f
        return inner
    '''
    Run the tasks.sort() method/
    Initialize a dictionary of completed.
        Iterate through each sorted task:
        Check every node in the graph, and if the task is referenced, run the task with the proper input and add it to completed.
        If the task is not referenced, run the task without arguments and add it to completed.
    Return the completed dictionary.
    '''
    def run(self):
        scheduled = self.tasks.sort()
        completed = {}
        
        for task in scheduled:
            for node, values in self.tasks.graph.items():
                if task in values:
                    completed[task] = task(completed[node])
            if task not in completed:
                completed[task] = task()
        return completed

pipeline = Pipeline()

# Wrapping functions with pipeline task method to assign run dependencies
@pipeline.task()
def parse_logs(logs):
    return parse_logs(logs)

@pipeline.task(depends_on=parse_logs)
def build_raw_csv(lines):
    return build_csv(lines, header=[
        'ip', 'time_local', 'request_type',
        'request_path', 'status', 'bytes_sent',
        'http_referrer', 'http_user_agent'
    ],
    # The StringIO object mimicks a file-like object that, instead of writing out to disk, 
    # keeps a file-like object in memory.
    file=io.StringIO())

@pipeline.task(depends_on=build_raw_csv)
def count_uniques(csv_file):
    return count_unique_request(csv_file)

@pipeline.task(depends_on=count_uniques)
def summarize_csv(lines):
    return build_csv(lines, header=['request_type', 'count'], file=io.StringIO())

outputs = pipeline.run()