def linearSearch(a_list, x):
    i, length=0, len(a_list)
    while i<length and x !=a_list[i]:
        i+=1
    return i if i<length else -1

a=range(1,11)
for i in a:
    print("{0} index {1}".format(i, linearSearch(a,i)))

print(linearSearch(a, 18))
print(linearSearch([], 1))
