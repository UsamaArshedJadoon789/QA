# Environment Setup and Verification
## 1. Java Environment
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
java -version  # Should show OpenJDK 17
```

## 2. Hadoop Environment
```bash
export HADOOP_HOME=/home/ubuntu/qa/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
hadoop version  # Should show Hadoop 3.3.6
```

## 3. Verification Steps
1. Source the environment script:
```bash
source documentation/hadoop/setup/environment/setup_env.sh
```

2. Verify environment variables:
```bash
echo $JAVA_HOME
echo $HADOOP_HOME
echo $PATH
```
