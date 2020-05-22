#Lab0-Program3b-liu1827
from random import *

def program3b():
    ans = randint(0,10)
    guess = []
    for i in range(0,3):
        guess.append(int(input("Enter your guess:"))) 
    result = list(filter(lambda x: (x == ans), guess))
    if (any(result)):
        print("You win!")
    else:
        print("You lose!")
    return    
        
if __name__ == "__main__":
    program3b()