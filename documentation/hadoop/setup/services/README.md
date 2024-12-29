# Hadoop Services Setup and Startup
## 1. Prerequisites
- Hadoop configuration files properly set up
- Environment variables configured
- SSH access configured

## 2. Service Startup Steps
### 2.1 Format HDFS (First time only)
```bash
hdfs namenode -format
```

### 2.2 Start HDFS Services
```bash
start-dfs.sh
```

### 2.3 Start YARN Services
```bash
start-yarn.sh
```

### 2.4 Verify Running Services
```bash
jps
```

Expected output:
```
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
```
