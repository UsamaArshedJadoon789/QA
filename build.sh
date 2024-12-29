#!/bin/bash

# Create build directory
mkdir -p build

# Compile Java files
javac -cp $(hadoop classpath) \
    src/main/java/com/jasminegraph/indegree/*.java \
    -d build/

# Create JAR file
jar -cvf indegree-computation.jar -C build/ .

echo "Build complete. JAR file created: indegree-computation.jar"
