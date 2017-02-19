"""
TripAdvisor Programming Challenge 2016
Author: Johnny Lau Tufts University '17

Implementation: 
  - Uses two heaps for jobs and workers.
  - Workers and jobs are keyed by how early they can work and be worked on, resp.
  - When a job is popped for the first time, it is split into two jobs if it can't be
    completed in time for the next job

TODO:
  - Priority is not being resolved
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
Aggregate worker time calculations
"""

"""Calculates available working hours between t1 and t2"""
def man_hours(workers, t1, t2):
  return sum(t2 - t1 if w.can_begin < t2 else w.can_begin for w in workers)

"""True if workers can complete job before specified time"""
def can_complete(workers, job, t):
  return man_hours(workers, job.can_begin, t) >= job.total_time()

"""Splits a job based on how much a set of workers can complete it up to t"""
def split(workers, job, t):
  mh = man_hours(workers, job.can_begin, t)
  if mh >= job.total_time():
    return (job, Job(job.name, 0, job.task_time, job.can_begin, job.priority))
  else:
    tasks_completeable = int(job.tasks * (float(mh) / job.total_time()))
    return (Job(job.name, tasks_completeable, job.task_time, job.can_begin, job.priority),
            Job(job.name, job.tasks-tasks_completeable, job.task_time, t, job.priority))

"""Takes the next len(workers) tasks and splits them into individual jobs to allow multithreading"""
def threadableSplit(workers, job):
  split_jobs = []
  new_begin = job.can_begin + job.task_time * job.tasks
  for w in workers:
    if (job.tasks == 0): break
    begin = job.can_begin if job.can_begin > w.can_begin else w.can_begin
    new_begin = min(begin, new_begin) + job.task_time
    j = Job(job.name, 1, job.task_time, begin, job.priority)
    split_jobs.append(j)
  if job.tasks != 0:
    job.tasks -= len(split_jobs)
    job.can_begin = new_begin
    split_jobs.append(job)
  return split_jobs


"""
Scheduling procedures
"""
def schedule(workers, jobs):
    schedule = []
    whq = [(w.can_begin, w) for w in workers]
    jhq = [(j.can_begin, j, False) for j in jobs] 
    heapify(whq)
    heapify(jhq)
    while jhq:
      print jhq
      (j_begin, j, checked) = heappop(jhq)
      if j.tasks == 0: continue
      if jhq:
        nxt = jhq[0][1]
        if not checked:
	  js = threadableSplit(workers, j)
	  for j in js:
            heappush(jhq, (j.can_begin, j, True))
	  continue
      checked = True
      (w_begin, w) = heappop(whq)
      if w_begin < j_begin:
        a = Assignment(j_begin,w,j)
	w.can_begin = j_begin + j.task_time
      else:
        a = Assignment(w_begin,w,j)
	w.can_begin += j.task_time
      j.tasks -= 1
      heappush(jhq, (j.can_begin, j, checked))
      heappush(whq, (w.can_begin, w))
      schedule.append(a)
    #return schedule  
    return _condense_schedule(workers, schedule)

"""Skips stretches of the same task by the same worker"""
def _condense_schedule(workers, s)
    if not s: []
    w_dict = {} # worker name -> job name
    for w in workers:
      w_dict[w.name] = None
    cs = []
    for a in s:
     if w_dict[a.worker.name] is None:
       cs.append(a)
       w_dict[a.worker.name] = a.job.name
     if w_dict[a.worker.name] != a.job.name:
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
