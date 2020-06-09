import math
import numpy as np
import pandas as pd
from scipy.misc import derivative

print('функция f(x)=ln(x)', '\n')
print('узлы: 1, 3, 5, 6, 8, 10 ', '\n')
print('Точка интерполирования: x = 7', '\n')
print('Порядок интерполирования n = 3', '\n')



def f(x):
    return round(math.log(x), 4)



def fun(arr):
    r1, r2, r3 = [], [], []  

    for j in range(len(arr) - 1):
        r1.append(round(((f(arr[j + 1]) - f(arr[j])) / (arr[j + 1] - arr[j])), 4))

    for j in range(len(arr) - 2):
        r2.append(round(((r1[j + 1] - r1[j]) / (arr[j + 2] - arr[j])), 4))

    for j in range(len(arr) - 3):
        r3.append(round(((r2[j + 1] - r2[j]) / (arr[j + 3] - arr[j])), 4))
    return r1, r2, r3



def printR(r1, r2, r3, arr):
    print('Таблица разделенных разностей(отсортированныe узлы):', '\n')
    print('{0:^6}{1:>6}{2:>6}{3:>8}{4:>7}'.format('x', 'f(x)', 'I', 'II', 'III'))
    for i in range(len(arr)):
        print('{0:<6} {1:<6}'.format(arr[i], f(arr[i])), end=' ')
        if i == 0:
            print('{0:<6} {1:<6} {2:<6}'.format(r1[0], r2[0], r3[0]))
        elif i == 1:
            print("{0:<6} {1:<6}".format(r1[1], r2[1]))
        elif i == 2:
            print("{0:<6}".format(r1[2]))



def polynomial(x, nodes, r1, r2, r3):
    values = [0] * 4
    values[0] = f(nodes[0])

    div = x - nodes[0]
    values[1] = values[0] + r1[0] * div

    div *= x - nodes[1]
    values[2] = values[1] + r2[0] * div

    div *= x - nodes[2]
    values[3] = values[2] + r3[0] * div
    return values


def actual_err(x, f, values):
    errors = [0] * 4
    for i in range(4):
        errors[i] = f(x) - values[i]
    return errors



def estimate_mod_der(n, x, nodes):
    modules = [0] * 4
    for i in range(n + 1):
        c = x
        d = x
        for j in range(i + 1):
            c = min(c, nodes[j])
            d = max(d, nodes[j])
        step = abs(c - d) / 50
        for k in np.arange(c + step, d, step):
            modules[i] = max(abs(derivative(f, k, dx=1.0, n=i + 1, order=n + 2)),
                             abs(derivative(f, k - step, dx=1.0, n=i + 1, order=n + 2)))
    return modules


def estimate_err(x, modules, nodes):
    est_errors = [0] * 4
    a = 1
    for i in range(4):
        a *= abs(x - nodes[i])
        est_errors[i] = modules[i] * a / math.factorial(i + 1)
    return est_errors



n = 3
x = 7

arr1 = 1, 3, 5, 6, 8, 10

arr2 = [] 
for i in arr1:
    arr2 += [abs(x - i)]

d = {}
for i in range(len(arr1)):
    d[arr1[i]] = arr2[i]


X = list(d.items())
X.sort(key=lambda i: i[1])

i = len(X) - n - 1
while i > 0:
    del X[len(X) - 1]
    i -= 1

xx = []
for i in X:
    xx.append(i[0])



r1, r2, r3 = fun(xx)
print('\n')
printR(r1, r2, r3, xx)


values = polynomial(x, xx, r1, r2, r3)
errors = actual_err(x, f, values)
modules = estimate_mod_der(n, x, xx)
est_errors = estimate_err(x, modules, xx)


pd.options.display.max_columns = 20
desired_width = 400
pd.set_option('display.width', desired_width)

print('\n')
data = [xx, values, errors, modules, est_errors]
s1 = 'Узлы в порядке очередности их использования:'
s2 = 'значение многочлена в точке интерполирования:'
s3 = 'фактическая погрешность:'
s4 = 'оценка модуля производной:'
s5 = 'оценка погрешности:'
indexes = [s1, s2, s3, s4, s5]

df = pd.DataFrame(data, index=indexes, columns=[i for i in range(4)])
df.columns.name = "i"

print(df)