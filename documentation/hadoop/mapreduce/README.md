# In-Degree Distribution Computation

## Overview
This MapReduce implementation calculates the in-degree distribution of nodes in a directed graph.

### Input Format
- Tab-separated text files
- Two columns: FromNodeId and ToNodeId
- Comments start with #

### Implementation Details
The implementation consists of two main components:

1. Mapper (`InDegreeMapper`)
   - Input: `<LongWritable, Text>` (line number, line content)
   - Output: `<Text, IntWritable>` (destination node, count of 1)
   - Skips comment lines (starting with #)
   - Splits each line on tab character
   - Emits destination node as key with count 1

2. Reducer (`InDegreeReducer`)
   - Input: `<Text, Iterable<IntWritable>>` (node, list of counts)
   - Output: `<Text, IntWritable>` (node, total in-degree)
   - Sums all counts for each node
   - Outputs final in-degree count

### Build Instructions
```bash
# Build the project
./build.sh

# Run tests
hadoop jar indegree-computation.jar com.jasminegraph.indegree.InDegreeComputation \
    test/data/sample_graph.txt \
    test/output
```

### Example Input
```
# FromNode ToNode
1    2
1    3
2    3
```

### Example Output
```
2    2  # Node 2 has in-degree 2
3    2  # Node 3 has in-degree 2
```
