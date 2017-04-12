"""
TripAdvisor Programming Challenge 2016
Author: Johnny Lau Tufts University '17

Implementation: 
  - This is a naive solution. 
  - Uses two heaps for jobs and workers.
  - Workers and jobs are keyed by how early they can work and be worked on, resp.

TODO:
  - Priority is not being resolved
  - How early a job can be worked on is a static value for all tasks...
"""
import sys, fileinput
from heapq import *

"""
Define a android
"""
class Android:
  def __init__(self, name):
    self.name = str(name)
    self.can_begin = 0

  def __repr__(self):
    return "worker {} {}".format(self.name, self.can_begin)

"""
Define a job
"""
class Job:
  def __init__(self, name, tasks, task_time, can_begin, priority):
    self.name = str(name)
    self.can_begin = int(can_begin)
    self.tasks = int(tasks)
    self.task_time = int(task_time)
    self.priority = int(priority)

  def total_time(self):
    return self.task_time * self.tasks

  def __repr__(self):
    return "job {} {} {} {} {}".format(
      self.name, self.tasks, self.task_time, self.can_begin, self.priority)

"""
Define an assignment
"""
class Assignment:
  def __init__(self, start_time, worker, job):
    self.start_time = start_time
    self.worker = worker
    self.job = job

  def __repr__(self):
    return "{} {} {}".format(
      self.start_time, self.worker.name, self.job.name)

  def __str__(self):
    return self.__repr__()

"""
Scheduling procedures
"""
def schedule(workers, jobs):
    schedule = []
    whq = [(w.can_begin, w) for w in workers]
    jhq = [(j.can_begin, j) for j in jobs] 
    heapify(whq)
    heapify(jhq)
    while jhq:
      j_begin, j = heappop(jhq)
      if j.tasks == 0: continue
      w_begin, w = heappop(whq)
      if w_begin < j_begin:
        a = Assignment(j_begin,w,j)
        w.can_begin = j_begin + j.task_time
      else:
        a = Assignment(w_begin,w,j)
        w.can_begin += j.task_time
      j.tasks -= 1
      heappush(jhq, (j.can_begin, j))
      heappush(whq, (w.can_begin, w))
      schedule.append(a)
    #return schedule  
    return _condense_schedule(workers, schedule)

"""Skips stretches of the same task by the same worker"""
def _condense_schedule(workers, s):
    if not s: return []
    w_dict = {w.name: None for w in workers} # worker name -> job name
    cs = []
    for a in s:
     cur_job = w_dict[a.worker.name]
     if cur_job is None or cur_job != a.job.name:
       cs.append(a)
       w_dict[a.worker.name] = a.job.name
    return cs

"""
Parsing Input
"""
def parseInput():
  jobs = []
  workers = []
  for line in fileinput.input():
    args = line.split()
    if args[0] == "job":
      j = Job(*args[1:])
      jobs.append(j)
    elif args[0] == "worker":
      w = Android(*args[1:])
      workers.append(w)
  return (workers, jobs)

def main():
  workers, jobs = parseInput()
  for s in schedule(workers, jobs):
    print s

if __name__ == '__main__':
  main()
