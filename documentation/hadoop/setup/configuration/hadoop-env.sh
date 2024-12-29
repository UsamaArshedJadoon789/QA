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
