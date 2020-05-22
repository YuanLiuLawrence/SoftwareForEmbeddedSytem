#Lab0-Program5-liu1827
def program5():
    nums = [10,20,10,40,50,60,70]
    val = int(input("What is your target number? "))
    nums_dict = {}
    check = 0
    for i, num in enumerate(nums):  
        if (val - num in nums_dict):
            index1 = nums_dict[val - num]
            index2 = i
            check = check + 1
            print("index1={}, index2={}".format(index1,index2))
        nums_dict[num] = i
    if (check == 0):
        print("Required numbers not found")
    return


if __name__ == "__main__":
    program5()