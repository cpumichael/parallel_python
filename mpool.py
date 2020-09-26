
import random
import time
from multiprocessing import Pool

def f(x):
    ret = '<>'.join(x)
    r = random.random()
    time.sleep(r * r)
    return ret

if __name__ == '__main__':
    with Pool(5) as p:
        for pp in p.map(f, (str(i) for i in range(101))):
            print(pp)

# vim: ai sw=4 ts=4 et showmatch
