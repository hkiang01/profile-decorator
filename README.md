# memory-profiler-viz


## Idea
Idea: [memory-profiler](https://pypi.org/project/memory-profiler/) vizualized like [jaeger traces](https://github.com/jaegertracing/jaeger-ui/blob/0c1fcd16af842fee63a8fdd061a3cc543701c61b/media/ss_trace.png)

![jaeger traces](https://github.com/jaegertracing/jaeger-ui/blob/0c1fcd16af842fee63a8fdd061a3cc543701c61b/media/ss_trace.png)

- Instead of Service & Operation lines, a file and line number
- Instead of a time axis that always goes up, a memory access that goes up and down
- Every new line is the next line of code run
