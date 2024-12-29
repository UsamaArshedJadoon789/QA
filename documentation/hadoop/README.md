# Hadoop Setup Documentation
## Installation and Configuration Guide
### Prerequisites
* Java 17 (OpenJDK)
* SSH Server
### Environment Variables
```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export HADOOP_HOME=/home/ubuntu/qa/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```
### Configuration Files
#### core-site.xml
Purpose: Defines HDFS filesystem URI and temporary directory location
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
#### hdfs-site.xml
Purpose: Configures HDFS replication and storage directories
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
#### mapred-site.xml
Purpose: Sets MapReduce framework and classpath configuration
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
#### yarn-site.xml
Purpose: Configures YARN resource management and node settings
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
### Installation Steps
1. Install Java and SSH
2. Configure SSH for localhost
3. Set environment variables
4. Configure Hadoop files
5. Format HDFS namenode
6. Start HDFS and YARN services
