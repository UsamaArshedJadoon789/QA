# Hadoop Setup Guide
## Prerequisites
* Java 17 (OpenJDK)
* SSH Server
## Environment Setup
```bash
# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Set HADOOP_HOME
export HADOOP_HOME=/home/ubuntu/qa/hadoop

# Add Hadoop bin directories to PATH
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Set HADOOP_CONF_DIR
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop

# Set HADOOP_MAPRED_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME

# Set HADOOP_COMMON_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME

# Set HADOOP_HDFS_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME

# Set YARN_HOME
export YARN_HOME=$HADOOP_HOME

# Set HADOOP_COMMON_LIB_NATIVE_DIR
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native

# Set HADOOP_OPTS
export HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native"
# End of configuration
```
## Configuration Files
### Core Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/ubuntu/qa/hadoop_tmp</value>
    </property>
</configuration>
```
### HDFS Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/ubuntu/qa/hadoop_tmp/dfs/name</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/ubuntu/qa/hadoop_tmp/dfs/data</value>
    </property>
</configuration>
```
### MapReduce Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
```
### YARN Configuration
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME</value>
    </property>
</configuration>
```
## Service Management
1. Format HDFS NameNode
2. Start HDFS services
3. Start YARN services
4. Verify running services
