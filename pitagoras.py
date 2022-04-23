def prime(n):
    i=2
    if n%i==0:
        return False
    while i*i <= n:
        if n % i == 0:
            return False
        i += 2
    return True 

    #print first 100 prime numbers
for i in range(1, 100000):
    if prime(i):
        print(i)