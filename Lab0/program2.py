#Lab0-Program2-liu1827
def program2():
    a = [1,1,2,3,5,8,13,21,34,55,89]
    num = int(input("Enter number: "))
    result = list(filter(lambda x: (x < num), a))
    print("The new list is {}".format(result))
    return

if __name__ == "__main__":
    program2()