def factorial(n):
    f = 0
    for i in range(n):
        f *= i
    return f

print(factorial(10))