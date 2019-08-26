from multiprocessing import Process
import os, time

a1='test'
def count(st,ed):
    for i in range(st,ed):
        c = a1 + str(i)
    print('Process %s ended.' %  os.getpid())
    time.sleep(3)

threadlist = []
a=1
while a<=90:
    b=a+10
    # count(a,b)
    name = 'thread' + str(a)
    t = Process(target=count,name=name,args=(a,b,))
    threadlist.append(t)
    a +=10

c1 = 1
for i in threadlist:
    i.start()
    if c1 == 3:
        i.join()
        c1=0
        print('c1:',c1)
        time.sleep(10)
    c1 += 1
i.join()