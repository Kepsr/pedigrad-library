import random
import timeit
import math

# n = 200

# indices = [i for i in range(n) if random.choice((True, False))]
# xs = [x ** 2 for x in range(n)]
# ys = [math.sqrt(x) for x in range(n)]

# def f():

#     new_xs = []
#     new_ys = []
#     for i, (x, y) in enumerate(zip(xs, ys)):
#         if i in indices:
#             new_xs.append(x)
#             new_ys.append(y)
#     return new_xs, new_ys

# def f2():

#     for i, (x, y) in enumerate(zip(xs, ys)):
#         if i in indices:
#             yield x, y

# def f3():
#     # xs, ys = map(list, zip(*f2()))
#     # return xs, ys
#     return tuple(map(list, zip(*f2())))

# def f4():
#     new_xs = []
#     new_ys = []
#     for x, y in f2():
#         new_xs.append(x)
#         new_ys.append(y)
#     return new_xs, new_ys

# def g():

#     new_xs = [x for i, x in enumerate(xs) if i in indices]
#     new_ys = [y for i, y in enumerate(ys) if i in indices]
#     return new_xs, new_ys

# def h():

#     new_xs, new_ys = map(list, zip(*(
#         (x, y) for i, (x, y) in enumerate(zip(xs, ys))
#         if i in indices
#     )))
#     return new_xs, new_ys

# funcs = [f, h, f3, f4]
# random.shuffle(funcs)

# assert all(func() == f() for func in funcs), [func() for func in funcs]
# for func in funcs:
#     print(f'{func.__name__:>4}: {timeit.timeit(func, number=int(2e4))}')


l = []
for x in range(10):
    l.extend([[19, *list(range(x))]])
#     l.extend([list(range(x))])
# for x in l:
    # x.insert(0, 19)
print(l)
