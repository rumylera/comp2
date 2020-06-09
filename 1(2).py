import math
import numpy as np
from scipy.misc import derivative
import pandas as pd
 
print('функция: f(x) = sin(x)')
print('отрезок: [-0.5 , 0.5]')
print('точка х: х = 0.45')
x = 0.45
a, b = -0.5, 0.5
print('Шаг интерполяции h = 0.1')
h = 0.1
print('Порядок интерполирования n = 4 ')
n = 4
 
 
pd.options.display.max_columns = 20
desired_width = 400
pd.set_option('display.width', desired_width)
 
 
def f(x):
    return round(math.sin(x), 5)
 
 
def delta(n, arr):
    diffs = [arr]
    for k in range(1, n + 1):
        arr1 = []
        for i in range(len(arr) - k):
            arr1.append(round(diffs[k - 1][i + 1] - diffs[k - 1][i], 5))
        diffs.append(arr1)
 
    return diffs
 
 
 
def table(n):
    arr = []
    for i in range(int((b - a) / h + 1)):
        arr.append(f(a + i * h))
 
    diffs = delta(n, arr)
 
 
    num = len(diffs[0]) - 1
    for i in range(1, len(diffs)):
        for j in range(len(diffs[i]) - 1, num):
            diffs[i].append(math.nan)
            j += 1
 
 
    columns = ['f(x)', '\u0394y', '\u03942y', '\u03943y', '\u03944y']
    data = {}
    for i in range(len(diffs)):
        data[columns[i]] = diffs[i]
    indexes = []
    for j in range(len(arr)):
        indexes.append(round(a + j * h, 1))
 
    df1 = pd.DataFrame(data, index=indexes)
    df1.columns.name = 'x'
    print(df1)
 
 
def coefficient(n, t):
    coefs = [0] * (n + 2)
    coefs[0] = 1
    for i in range(1, n + 2):
        y = 1
        for j in range(1, i + 1):
            y *= (t - ((-1) ** j) * (j // 2)) / j
        coefs[i] = round(y, 5)
    return coefs
 
 
 
def polynomial(n, t, coefs):
    values = [0] * (n + 1)
    arr = []
    for i in range(7):
        arr.append(f(a + h * (i - 3)))
 
    diffs = delta(n, arr)
 
    values[0] = diffs[0][len(diffs[0]) // 2]
    for i in range(1, n + 1):
        y = coefs[i]
        y *= diffs[i][(len(diffs[0]) // 2) - (i // 2)]
        y = round(y, 5)
        values[i] = values[i - 1] + y
 
    difference = []
    for j in range(n + 1):
        difference.append(diffs[j][(len(diffs[0]) // 2) - (j // 2)])  # используемые разделенные разности
 
    p_coefs = []
    for j in range(n + 1):
        p_coefs.append(round(coefs[j] * diffs[j][(len(diffs[0]) // 2) - (j // 2)], 5))
 
    return difference, p_coefs, values
 
 
 
def estimate_mod_der(n):
    modules = [0] * (n + 1)
    modules[0] = abs(derivative(f, a, dx=1.0, n=1, order=n + 3))
    for i in range(1, n + 1):
        c = a
        d = a + i * h
        step = abs(c - d) / 50
        for k in np.arange(c + step, d, step):
            modules[i] = max(abs(derivative(f, k, dx=1.0, n=i + 1, order=n + 3)),
                             abs(derivative(f, k - step, dx=1.0, n=i + 1, order=n + 3)))
    return modules
 
 
def estimate_err(modules, coefs):
    est_errors = [0] * (n + 1)
    for i in range(n + 1):
        est_errors[i] = round(modules[i] * abs(coefs[i + 1]) * h ** (i + 1), 5)
    return est_errors
 
 
 
table(n) 
 
 
t = (x - a) / h
 
coefs = coefficient(n, t)
difference, p_coefs, values = polynomial(n, t, coefs)
errors = []
for j in range(n + 1):
    errors.append(round(f(x) - values[j], 5))  
 
modules = estimate_mod_der(n)
est_errors = estimate_err(modules, coefs)
 
s1 = 'коэффициенты N_k полинома'
s2 = 'используемые разделенные разности'
s3 = 'N_k * \u0394k(y0) '
s4 = 'значения полинома'
s5 = 'фактическая погрешность'
s6 = 'оценка погрешности'
 
del coefs[len(coefs) - 1]  
data = [coefs, difference, p_coefs, values, errors, est_errors]
 
indexes = [s1, s2, s3, s4, s5, s6]
 
df = pd.DataFrame(data, index=indexes, columns=[i for i in range(5)])
df.columns.name = 'k'
 
print('\n')
print(df)