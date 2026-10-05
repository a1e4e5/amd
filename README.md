# amd
Basid fault scenarios:
1) Thread contention / hot lock: [not implemented]. Planned scenario: multithreading used for writing to the same file.
2) IO contention - Multiprocessing used for writing to the same file, with flushing to disk very small amount of data. Fixed version collects many results before writing data to disk (batching).
3) CPU contention - while() true loop. Example from real production ;). Fixed version uses sleep and checks condition every second, not permanently.
4) TOCTOU - fault scenario implemented (src.jobs.hazard), test not. Expected exception on stress testing when multithreading is applied.
5) Deadlock - not implemented.

src.fault.flags to toggle between bad and good behavior.

Benchmark chart (from one test only): https://a1e4e5.github.io/amd/dev/bench/
