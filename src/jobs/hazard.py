
import random
import time

from src.fault_flags import TOC_TOU
from src.runner import PRIORITY_2, MultiRunner

common_list = list(range(100000))

def get_from_list():
    global common_list
    while True:
        x = len(common_list)
        if x == 0:
            common_list = list(range(100000))       # restore new list
            break
        # print(f"Going to get last elem from common list, current len is {x}")
        y = random.uniform(0.001, 0.01)
        time.sleep(y)
        if TOC_TOU:
            common_list.pop(x-1)             # take last by index, but list might have beed shortened already
        else:
            common_list.pop(-1) if common_list else None     # take last element, regardless of len



def main():
    runner = MultiRunner(max_p1_workers=10, max_p2_workers=10, mode='threading')
    runner.add_function('get_from_list', get_from_list())
    for _ in range(10):
        runner.add_task('get_from_list', PRIORITY_2, ())
    runner.run()

if __name__ == '__main__':
    main()
