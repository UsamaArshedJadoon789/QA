# Hadoop Configuration Documentation
## Environment Setup
* JAVA_HOME: /usr/lib/jvm/java-17-openjdk-amd64
* HADOOP_HOME: /home/ubuntu/qa/hadoop
## Configuration Files
### core-site.xml
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
Purpose: Defines HDFS filesystem URI and temporary directory location.
### hdfs-site.xml
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
Purpose: Configures HDFS replication and storage directories.
### mapred-site.xml
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
Purpose: Sets MapReduce framework and classpath configuration.
### yarn-site.xml
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
Purpose: Configures YARN resource management and node settings.