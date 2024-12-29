# Hadoop Service Management
## 1. Service Control Commands
### 1.1 Start Services
```bash
start-dfs.sh    # Start HDFS services
start-yarn.sh   # Start YARN services
```

### 1.2 Stop Services
```bash
stop-yarn.sh    # Stop YARN services
stop-dfs.sh     # Stop HDFS services
```

## 2. Service Status Verification
```bash
jps            # List Java processes
```

## 3. Service Logs
Log files location: `/home/ubuntu/qa/hadoop/logs/`

## 4. Common Issues
1. Services won't stop: Check for stale process IDs
2. Services fail to start: Check logs for errors
3. Resource Manager unavailable: Verify YARN configuration
