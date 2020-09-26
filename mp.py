from multiprocessing import Process
import os

def f(name, x):
    print('I am child: hello', name, x, 'pid=', os.getpid(), 'ppid=', os.getppid())

if __name__ == '__main__':
    print('PARENT pid=', os.getpid(), 'ppid=', os.getppid())
    p = Process(target=f, args=('bob', 'rabbit'))
    p.start()
    p.join()


