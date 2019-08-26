#!/bin/bash/env python

import threading,os,time

a1='test'
def count(st,ed):
    for i in range(st,ed):
        c = a1 + str(i)
    print('thread %s ended.' % threading.current_thread().name)
    time.sleep(3)

threadlist = []
a=1
while a<=90:
    b=a+10
    # count(a,b)
    name = 'thread' + str(a)
    t = threading.Thread(target=count,name=name,args=(a,b,))
    threadlist.append(t)
    a +=10

c1 = 1
for i in threadlist:
    i.setDaemon(True)
    i.start()
    if c1 == 3:
        i.join()
        c1=0
        print('c1:',c1)
        time.sleep(10)
    c1 += 1
i.join()