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
            idx = self.tasks.index(depends_on) + 1
        def inner(f):
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
    return parse_log(logs)

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