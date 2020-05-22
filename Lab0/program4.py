#Lab0-Program4-liu1827
def program4():
    date = {
        "Albert Einstein": "03/14/1879",
        "Benjamin Franklin": "01/17/1706",
        "Ada Lovelace": "12/10/1815"
        }
    print("Welcome to the birthday dictionary. We know the birthdays of:")
    print("Albert Einstein");
    print("Benjamin Franklin");
    print("Ada Lovelace");
    name = input("Who’s birthday do you want to look up?\n")
    print("{}'s birthday is {}.".format(name, date[name]))
    return
    
if __name__ == "__main__":
    program4()