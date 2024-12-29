#!/bin/bash

# Clean previous test output
rm -rf test/output

# Run MapReduce job on test data
hadoop jar indegree-computation.jar \
    com.jasminegraph.indegree.InDegreeComputation \
    test/data/sample_graph.txt \
    test/output

# Display results
echo "=== Test Results ==="
cat test/output/part-r-00000
