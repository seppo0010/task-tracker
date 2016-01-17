import csv
import datetime
import sys
import time

def parse_date(date):
    return time.mktime(time.strptime(date, '%Y-%m-%d'))

def format_time(t):
    return datetime.date.fromtimestamp(t).strftime('%Y-%m-%d');

class Task(object):
    done = False
    name = None
    identifier = None
    start_date = None
    end_date = None
    dependencies = None

    def __init__(self, row):
        self.done = row[0] == '1'
        self.name = row[1]
        self.identifier = row[2]
        self.start_date = parse_date(row[3]) if len(row) > 3 and len(row[3]) > 0 else None
        self.end_date = parse_date(row[4]) if len(row) > 4 and len(row[4]) > 0 else None
        self.dependencies = row[5].split(',') if len(row) > 5 and len(row[5]) > 0 else []

    def is_available(self, tasks):
        if self.start_date is not None or self.start_date > time.time():
            return False
        for d in self.dependencies:
            if not tasks[d].done:
                return False
        return True

    def is_leaf(self, tasks):
        for task in tasks.values():
            if self.identifier in task.dependencies:
                return False
        return True

    def range_string(self):
        if self.start_date is not None and self.end_date is None:
            return 'since ' + format_time(self.start_date)
        elif self.end_date is not None and self.start_date is None:
            return 'until ' + format_time(self.end_date)
        elif self.end_date is not None and self.start_date is not None:
            return format_time(self.start_date) + ' to ' + format_time(self.end_date)
        return None

    def task_view(self, tasks, indentation=0):
        range_string = self.range_string()
        return ''.join((
                ' ' * indentation * 2,
                self.name,
                ' (' + range_string + ')' if range_string is not None else '',
                '\n',
                '\n'.join(tasks[t].task_view(tasks, indentation + 1) for t in self.dependencies if not tasks[t].done)
                ))

    def __repr__(self):
        return str(self.__dict__)


def parse_csv(path):
    tasks = {}
    with open(path, 'rb') as csvfile:
        for row in csv.reader(csvfile):
            task = Task(row)
            tasks[task.identifier] = task
    return tasks

def show_available(tasks):
    for task in tasks.values():
        if task.is_available(tasks) and not task.done:
            print task.task_view(tasks)

def show_deadlines(tasks):
    for task in tasks.values():
        if task.end_date is not None and task.is_leaf(tasks):
            print task.task_view(tasks)

def show_help(tasks):
    print 'task-tracker.py <filename> [available|deadlines]'

if __name__ == '__main__':
    tasks = parse_csv(sys.argv[1])
    # TODO: use optparse, argparse or something more serious?
    if len(sys.argv) == 2:
        print tasks
    elif len(sys.argv) == 3:
        {
            'available': show_available,
            'deadlines': show_deadlines,
        }.get(sys.argv[2], show_help)(tasks)
