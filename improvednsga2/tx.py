import time

import ray

@ray.remote(num_returns=2)
def f2():
    time.sleep(1)
    return [1,2]


'''def f1():
    time.sleep(1)
    return 1
start = time.time()
results = [f1() for i in range(4)]
end = time.time()
chain_cost = end - start
print(chain_cost)

ray.init()
start = time.time()
results2 = []
for i in range(2):
    a,b = f2.remote()
    results2.append(ray.get(a))
    results2.append(ray.get(b))
    c, d = f2.remote()
    results2.append(ray.get(c))
    results2.append(ray.get(d))
end = time.time()
paral_cost = end - start
print(paral_cost)
print(results2)'''


@ray.remote
class Counter(object):
    def __init__(self):
        self.n = 0

    def increment(self):
        self.n += 2

    def read(self):
        return self.n

counters = [Counter.remote() for i in range(4)]
[c.increment.remote() for c in counters]
futures = [c.read.remote() for c in counters]
print(ray.get(futures))

#children = ray.get([self.generate() for x in range()])