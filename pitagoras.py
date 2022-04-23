def prime(n):
    i=2
    if n%i==0:
        return False
    i += 1
    while i*i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

    #print first 100 prime numbers
for i in range(1, 1000000):
    if prime(i):
        print(i)