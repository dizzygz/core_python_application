#!/usr/bin/env python
# -*- coding:utf-8 -*-

from atexit import register
from random import randrange
from threading import BoundedSemaphore, Lock, Thread
from time import sleep, ctime

lock = Lock()
MAX = 5
candytray = BoundedSemaphore(MAX)  # 糖果槽

def refill():
    lock.acquire()
    print 'Refilling candy...',
    try:
        candytray.release()  # 添加糖果
    except ValueError:
        print 'full, skipping'
    else:
        print 'OK'
    lock.release()

def buy():
    lock.acquire()
    print 'Buying candy...',
    if candytray.acquire(False):  # 拿走糖果,False的意思是,如果拿光了,不会被阻塞
        print 'OK'
    else:
        print 'empty, skipping'
    lock.release()

def producer(loops):
    for i in xrange(loops):
        refill()
        print 'free candytray num', candytray._Semaphore__value
        sleep(randrange(3))

def consumer(loops):
    for i in xrange(loops):
        buy()
        print 'free candytray num', candytray._Semaphore__value
        sleep(randrange(3))

def _main():
    print 'starting at:', ctime()
    nloops = randrange(2, 6)
    print 'free candytray num', candytray._Semaphore__value  # 获取当前空闲的糖果槽数(信号量计数器的值)
    print 'THE CANDY MACHINE (full with %d bars)!' % MAX
    Thread(target=consumer, args=(randrange(
        nloops, nloops+MAX+12),)).start() # buyer
    Thread(target=producer, args=(nloops,)).start() # vendor

@register
def _atexit():
    print 'all DONE at:', ctime()

if __name__ == '__main__':
    _main()
