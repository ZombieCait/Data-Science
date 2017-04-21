import heapq
def heapsort(a_list):
    h = []
    for value in a_list:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]

a=[1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
b=heapsort(a)
print(b)