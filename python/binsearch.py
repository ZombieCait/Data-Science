def binsearch(a_list, x,left,right):
    if left>right or len(a_list)==0:
        return -1;
    middle=(left+right)//2
    if a_list[middle]==x:
        return middle
    elif (a_list[middle]<x):
        return binsearch(a_list, x, middle + 1, right)
    else:
        return binsearch(a_list, x, left, middle - 1)


numbers=[]
print(numbers)

for number in numbers:
    print("{0} index {1}".format(number, binsearch(numbers, number,0, len(numbers)-1)))
