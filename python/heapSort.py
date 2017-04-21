import random
def heapSort(a_list):
    length=len(a_list)-1
    leastParent=length//2
    for i in range(leastParent, -1,-1):
        moveDown(a_list, i, length)

    for i in range(length, 0, -1):
        if a_list[0]>a_list[i]:
            swap(a_list, 0, i)
            moveDown(a_list, 0, i-1)

def moveDown(a_list, first, last):
    largest=2*first+1
    while largest<=last:
        if(largest<last) and (a_list[largest]<a_list[largest+1]):
            largest+=1
        if a_list[largest]>a_list[first]:
            swap(a_list, largest, first)
            first=largest
            largest=2*first+1
        else:
            return


def swap(A, i, j):
    tmp = A[i]
    A[i] = A[j]
    A[j] = tmp

numbers=[random.randint(0,1000) for r in range(1, 1000)]
print(numbers)
heapSort(numbers)
print(numbers)