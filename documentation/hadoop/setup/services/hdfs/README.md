# HDFS Setup and Verification
## 1. HDFS Formatting Process
```bash
# Format the namenode
hdfs namenode -format
```

## 2. Directory Structure
Required directories:
- NameNode directory: `/home/ubuntu/qa/hadoop_tmp/dfs/name`
- DataNode directory: `/home/ubuntu/qa/hadoop_tmp/dfs/data`

## 3. Verification Steps
1. Check HDFS directory structure
2. Verify namenode formatting
3. Start HDFS services
4. Check service status

## 4. Common Issues
1. Permission denied: Ensure proper directory ownership
2. Namenode fails to start: Check logs and reformat if necessary
3. DataNode not starting: Verify configuration and directory permissions
