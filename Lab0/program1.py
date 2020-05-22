#Lab0-Program1-liu1827
def program1():
    name = input("What is your name? ")
    age = int(input("How old are you? "))
    print("{} will be 100 years old in the year {}".format(name, 100-age+2019))
    return

if __name__ == "__main__":
    program1()