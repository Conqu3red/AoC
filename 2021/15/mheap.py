from typing import *

class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...

CT = TypeVar('CT', bound=Comparable)
T = TypeVar('T')

def compute_insertion_pos(l: List[CT], target: CT) -> int:
    left = 0
    length = len(l)
    if length == 0: return 0
    right = length - 1
    
    mid = 0

    while True:
        if left > length - 1:
            # not in list, add to end
            return length
        elif right < 0:
            # not in list, add to beginning
            return 0
        elif left > right:
            # not in list, but there is a good place to put it that isn't beyond either end
            return mid
        
        mid = (left + right) >> 1

        if l[mid] < target: # move ->
            left = mid + 1
        elif l[mid] > target: # move <-
            right = mid - 1
        else:
            # exact match found
            return mid

def heappush(heap: List[T], item: T):
    pos = compute_insertion_pos(heap, item)
    heap.insert(pos, item)

def heappop(heap: List[T]) -> T:
    return heap.pop(0)