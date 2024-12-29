# Hadoop Setup and Execution Screenshots

## Setup

### Java and Hadoop Installation Details
* OpenJDK 1.8.0_432 (64-bit) - Required for Hadoop compatibility
* Hadoop 3.3.6 - Latest stable release used for implementation
* Installation verified through version checks and environment validation
* All native libraries properly loaded and configured

## Configuration

### Core Configuration (core-site.xml)
* fs.defaultFS: hdfs://localhost:9000 - HDFS namenode location
* hadoop.tmp.dir: /home/ubuntu/qa/hadoop/tmp - Temporary directory for Hadoop operations
* dfs.permissions.enabled: false - Simplified permissions for testing environment

### HDFS Configuration (hdfs-site.xml)
* dfs.replication: 1 - Single replication factor for testing setup
* dfs.namenode.name.dir: /home/ubuntu/qa/hadoop/dfs/name - NameNode metadata storage
* dfs.datanode.data.dir: /home/ubuntu/qa/hadoop/dfs/data - DataNode block storage

### MapReduce Configuration (mapred-site.xml)
* mapreduce.framework.name: yarn - Using YARN as execution framework
* mapreduce.map.memory.mb: 1024 - Memory allocation for map tasks
* mapreduce.reduce.memory.mb: 1024 - Memory allocation for reduce tasks

### YARN Configuration (yarn-site.xml)
* yarn.nodemanager.aux-services: mapreduce_shuffle - Enable shuffle service
* yarn.scheduler.minimum-allocation-mb: 1024 - Minimum container size
* yarn.scheduler.maximum-allocation-mb: 8192 - Maximum container size

## Execution

### HDFS Status and Health
* Total Capacity: 124.93 GB
* Used Space: 131.65 MB (0.12%)
* Available Space: 111.35 GB
* Healthy Node Count: 1 (localhost)
* Block Replication Status: All blocks properly replicated
* Last Contact Time: Sun Dec 29 04:35:12 UTC 2024

## Performance Metrics

### System Resource Usage
* Memory: 7.8GB total with 4.4GB used
* CPU: 93.8% idle during normal operation
* Disk I/O: Sustained read/write operations
* Network: Local processing with minimal network overhead

### MapReduce Job Performance
* Job Completion Status: Successful
* Input Processing Rate: Varies by dataset
* Resource Utilization: Efficient memory and CPU usage
* Data Locality: Optimized for local processing
* Error Rate: Zero errors during processing

### Configuration Impact
* Single replication factor reduces storage requirements
* Local filesystem configuration minimizes network overhead
* Memory settings balanced for optimal resource utilization
* YARN container sizes appropriate for dataset processing
