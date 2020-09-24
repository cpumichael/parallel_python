from multiprocessing import Process

def f(name, x):
    print('hello', name, x)

if __name__ == '__main__':
    p = Process(target=f, args=('bob', 'rabbit'))
    p.start()
    p.join()


