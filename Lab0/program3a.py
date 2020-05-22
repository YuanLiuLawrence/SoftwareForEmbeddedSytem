#Lab0-Program3a-liu1827
def program3a():
    num = int(input("How many Fibonacci numbers would you like to generate? "))
    result = [1,1]
    if (num == 0):
        print("The Fibonacci Sequence is: ")
        return
    if (num == 1):
        result.pop(1)
    while(num > 2):
        result.append(result[-1]+result[-2])
        num = num - 1
    print("The Fibonacci Sequence is: {}".format(result))
    return 


if __name__ == "__main__":
    program3a()