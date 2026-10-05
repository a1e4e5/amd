"""
Simple runner for processing tasks simultanously.

Handles two pools:
- one for many, normal priority, medium heavy tasks
- one for short, high priority tasks
"""


import time
from concurrent.futures import ProcessPoolExecutor, as_completed

PRIORITY_1 = 1
PRIORITY_2 = 2

class MultiRunner:
    def __init__(self, max_p1_workers=1, max_p2_workers=10):
        self.runner_functions = {}                          # list of registered functions
        self.max_p1_workers = max_p1_workers         # for high priority short tasks
        self.max_p2_workers = max_p2_workers       # for heavy load but lower/normal priority
        self.tasks = []     # list of tasks [(f_name, priority, args)]
        self.p1_tasks = None
        self.p2_tasks = None
        self.future_results = {}
        self.results = []

    def add_function(self, name: str, func):
        """Register new function."""
        self.runner_functions[name] = func

    def add_task(self, f_name, priority, args):
        task = (f_name, priority, args)
        self.tasks.append(task)

    def _split_tasks(self):
        """Split tasks into two groups based on priority. Save in self.p1_tasks and self.p2_tasks."""
        self.p1_tasks = [t for t in self.tasks if t[1] == PRIORITY_1]
        self.p2_tasks = [t for t in self.tasks if t[1] == PRIORITY_2]
        assert len (self.tasks) == len(self.p1_tasks) + len(self.p2_tasks), "All tasks should be either P1 or P2"

    def _submit_tasks(self, executor, task_list):
        for order, task in enumerate(task_list):
            f_name, _, args = task          # priority logic applied earlier
            func = self.runner_functions[f_name]
            submission_time = time.perf_counter()
            future = executor.submit(func, *args)
            self.future_results[future] = (f_name, order, submission_time)

    def run(self):
        """
        Run tasks simultaneously. Gather results.
        Param 'tasks' should be a list of tuples: [(function_name: str, (function_args,)), ... ]
        """
        self._split_tasks()
        with ProcessPoolExecutor(max_workers=self.max_p1_workers) as priority_executor, \
                ProcessPoolExecutor(max_workers=self.max_p2_workers) as normal_executor:

            self._submit_tasks(priority_executor, self.p1_tasks)
            self._submit_tasks(normal_executor, self.p2_tasks)

            # collect results
            for future in as_completed(self.future_results):
                f_name, task_order, submission_time = self.future_results[future]
                duration_with_queue = time.perf_counter() - submission_time

                try:
                    res = future.result()
                    self.results.append({
                        "error_code": 0,
                        "result": res,
                        "duration_with_queue": duration_with_queue,
                        "duration": res[0],
                        "f_name": f_name,
                        "task_order": task_order,
                    })
                except Exception as e:      # noqa: BLE001
                    self.results.append({
                        "result": f"Exception: {e}",
                        "error_code": 1,
                        "duration_with_queue": duration_with_queue,
                    })


