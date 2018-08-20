from matplotlib import pyplot as plt
from tqdm import tqdm

'''Utility Functions'''

# Generates a random list of integers.
def rand_list(n, low=0, high=100):
    from random import randint
    return [ randint(1, n) for _ in range(n) ]


#Calculates the run time for a function f given input A.
def sort_time(f,A):
    from time import time
    from random import shuffle

    shuffle(A)
    start = time()
    f(A)
    stop = time()
    return stop - start


# Calculates the average run time for 1000 function calls.
def avg_sort_time(f,A, trials = 500):
    avg = 0
    for i in range(trials):
        avg += sort_time(f, A)
    return avg / trials


# Checks if the list is in ascending sorted order.
def is_sorted(A):
    for i in range(1, len(A)):
        if A[i] < A[i-1]:
            return False
    return True


'''Sorting Algorithms'''


# Worst case : O(N^2)
def insertion_sort(A):
    for j in range(len(A)):
        key, i = A[j], j - 1
        while i > -1 and A[i] > key:
            A[i+1], i = A[i], i - 1
        A[i+1] = key
    return A


#Worst case : O(N^2)
def bubble_sort(A):
    unsorted, j = True, len(A)
    while unsorted:
        unsorted = False
        for i in range(1,j):
            if A[i] < A[i-1]:
                A[i], A[i-1], unsorted = A[i-1], A[i], True
        j -= 1
    return A


#Worst case: O(N^2)
def selection_sort(A):
    for k in range(len(A)):
        mnmm, i = float('infinity'), -1
        for j in range(k, len(A)):
            if A[j] < mnmm:
                mnmm, i = A[j], j
        A[k], A[i]  = A[i], A[k]
    return A


#Worst case: O(NlogN)
def heap_sort(A):
    def sift_down(A, parent, upto):
        larger = 2 * parent + 1
        while larger < upto:
            if A[larger] < A[larger + 1]:
                larger += 1        
            if A[larger] > A[parent]:
                A[larger], A[parent] = A[parent], A[larger]
                parent = larger
                larger = 2 * parent + 1
            else:
                break
    last_node = len(A) - 1
    last_parent = last_node // 2
    [ sift_down(A, i, last_node) for i in range(last_parent, -1, -1) ]
    for i in range(last_node, 0, -1):
        if A[0] > A[i]:
            A[0], A[i] = A[i], A[0]
            sift_down(A, 0, i - 1)
    return A


#Worst case: O(NlogN)
def merge_sort(A):
    if len(A)>1:
        mid = len(A)//2
        lh, rh = A[:mid], A[mid:]
        merge_sort(lh)
        merge_sort(rh)
        i,j,k=0,0,0
        while i < len(lh) and j < len(rh):
            if lh[i] < rh[j]:
                A[k], i = lh[i], i + 1
            else:
                A[k], j = rh[j], j + 1
            k += 1
        while i < len(lh):
            A[k], i, k = lh[i], i + 1, k + 1
        while j < len(rh):
            A[k], j, k = rh[j], j + 1, k + 1
    return A

# Worst case: O(NlogN)
def quick_sort(A):
    def quick_sort_helper(A,first,last):
        if first<last:
            sp = partition(A,first,last)
            quick_sort_helper(A,first,sp-1)
            quick_sort_helper(A,sp+1,last)
    def partition(A,first,last):
        pv, lm, rm, done = A[first], first+1, last, False
        while not done:
            while lm <= rm and A[lm] <= pv:
                lm += 1
            while rm >= lm and A[rm] >= pv:
                rm -= 1
            if rm < lm:
                done = True
            else:
                A[lm], A[rm] = A[rm], A[lm]
        A[first], A[rm] = A[rm], A[first]
        return rm
    quick_sort_helper(A,0,len(A)-1)
    return A


# Worst case: O(kN)
def radix_sort(A):
    mod, div = 10, 1
    while True:
        buckets = [list() for _ in range(10)]
        [buckets[(n % mod) // div].append(n) for n in A]
        mod, div = mod * 10, div * 10
        if len(buckets[0]) == len(A):
            return buckets[0]
        A = []
        [A.append(y) for x in buckets for y in x]


# Used for comparison purposes.
def tim_sort(A):
    return sorted(A)
 

if __name__ == '__main__':

    # input list sizes used to generate random lists.
    input_sizes = [i for i in range(100, 5000, 500)]

    # Calculate the run times for the different sorting algorithms given the input sizes.
    sort_times = {
            'bubble_sort' : [ sort_time(bubble_sort, rand_list(i) ) for i in tqdm(input_sizes,'bubble_sort') ],
            'selection_sort' : [ sort_time(selection_sort, rand_list(i) ) for i in tqdm(input_sizes, 'selection_sort') ],
            'insertion_sort' : [ sort_time(insertion_sort, rand_list(i) ) for i in tqdm(input_sizes, 'insertion_sort') ],
            'merge_sort' : [ sort_time(merge_sort, rand_list(i) ) for i in tqdm(input_sizes, 'merge_sort') ],
            'heap_sort' : [ sort_time(heap_sort, rand_list(i) ) for i in tqdm(input_sizes, 'heap_sort') ],
            'quick_sort' : [ sort_time(quick_sort, rand_list(i) ) for i in tqdm(input_sizes, 'quick_sort') ],
            'radix_sort' : [ sort_time(radix_sort, rand_list(i) ) for i in tqdm(input_sizes, 'radix_sort') ]
    }

    for sort in sort_times:
        plt.plot(input_sizes, sort_times[sort], label = sort.replace('_', ' ').title() )

    plt.legend(loc='lower right')
    plt.show()