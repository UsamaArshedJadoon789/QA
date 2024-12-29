# Hadoop Process Management and Troubleshooting
## 1. Handling Stale Processes
```bash
# Remove stale PID files
sudo rm -f /tmp/hadoop-ubuntu-*.pid

# Kill stale processes
ps aux | grep "namenode" | grep -v grep | awk '{print $2}' | xargs -r kill -9
```

## 2. Clean HDFS Directories
```bash
rm -rf hadoop_tmp/dfs/name/* hadoop_tmp/dfs/data/*
mkdir -p hadoop_tmp/dfs/name hadoop_tmp/dfs/data
```

## 3. Format HDFS
```bash
hdfs namenode -format
```
