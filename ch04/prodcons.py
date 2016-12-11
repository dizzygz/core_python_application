#!/usr/bin/env python
# -*- coding:utf-8 -*-


from random import randrange
from time import sleep
from Queue import Queue
from myThread import MyThread
from threading import Lock

lock = Lock()

def writeQ(queue):
    queue.put('xxx', 1)
    with lock:
        print 'producing object for Q...',
        print "size now", queue.qsize()

def readQ(queue):
    val = queue.get(1)
    with lock:
        print 'consumed object from Q... size now', queue.qsize()
        print val

def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randrange(2, 6))

def reader(queue, loops):
    for i in range(loops):
        readQ(queue)

funcs = [writer, reader]
nfuncs = range(len(funcs))

def main():
    nloops = randrange(2, 20)
    q = Queue(32)

    threads = []
    for i in nfuncs:
        t = MyThread(funcs[i], (q, nloops), \
            funcs[i].__name__)
        threads.append(t)

    for i in nfuncs:
        threads[i].start()

    for i in nfuncs:
        threads[i].join()

    print 'all DONE'

if __name__ == '__main__':
    main()
