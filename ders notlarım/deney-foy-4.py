import math

def formul1():
    a = int(input("a değeri: "))
    b = int(input("b değeri: "))
    return ((math.sin(b) + (3 * math.pow(a,4))) / math.sqrt(a + b))


def formul2():
    x = int(input("x değeri: "))
    y = int(input("y değeri: "))
    sonuc = 0
    if x > y:
        sonuc += (x + y)
    elif x == y:
        sonuc += (x - y)
    elif x < y:
        sonuc += math.factorial(x+y)

    print(sonuc)

def formul3():
    sonuc = 0
    for i in range(1,11):
        b = i + 2
        sonuc += math.sqrt(i * b)
    print(sonuc)

#total = formul1()
#formul2()
#formul3()