import time
import random

t0 = time.time()
randomlist = []

for i in range(0,100000):
    n = random.randint(1,100000)
    randomlist.append(n)

t1 = time.time()

total = t1-t0
print("time: ", total)