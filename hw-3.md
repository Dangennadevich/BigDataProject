## ДЗ - 3

1. (hadoop:jn) Скачиваем дистрибутив Hive 4.0.1 на jump node 

```wget https://dlcdn.apache.org/hive/hive-4.0.1/apache-hive-4.0.1-bin.tar.gz```

2. (hadoop:jn) Разархивируем дистрибутив для apache-hive

```tar -xvzf apache-hive-4.0.1-bin.tar.gz ```

3. (hadoop:jn) Добавим переменную окружения HIVE_HOME и PATH

```export HIVE_HOME=/home/hadoop/apache-hive-4.0.1-bin```
```export PATH=$HIVE_HOME/bin:$PATH```

4. (hadoop:jn -> hadoop:nn) Создаем директорию в hdfs

```ssh 192.168.1.75```
```hdfs dfs -mkdir -p /user/hive/warehouse```

5. (hadoop:nn) Выдаем нужные права на директории в hdfs

```hdfs dfs -chmod g+w /user/hive/warehouse```
```hdfs dfs -chmod g+w /tmp```

6. (hadoop:jn) Копируем конфиг

```cp apache-hive-4.0.1-bin/conf/hive-default.xml.template apache-hive-4.0.1-bin/conf/hive-site.xml```

7. (hadoop:jn) Редактируем конфиг

```vim apache-hive-4.0.1-bin/conf/hive-site.xml```

Редактируем/добавляем property
```
  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
    <description>Defines the rewrite policy, the valid values are those defined in RewritePolicy enum</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionUserName</name>
    <value>hive</value>
    <description>Username to use against metastore database</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionURL</name>
    <value>jdbc:postgresql://team-18-nn:5432/metastore</value>
    <description>
      JDBC connect string for a JDBC metastore.
      To use SSL to encrypt/authenticate the connection, provide database-specific SSL flag in the connection URL.
      For example, jdbc:postgresql://myhost/db?ssl=true for postgres database.
    </description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionPassword</name>
    <value>hive</value>
    <description>password to use against metastore database</description>
  </property>
  <property>
    <name>javax.jdo.option.ConnectionDriverName</name>
    <value>org.postgresql.Driver</value>
    <description>Driver class name for a JDBC metastore</description>
  </property>
  <property>
    <name>hive.server2.thrift.port</name>
    <value>5433</value>
    <description>Port number of HiveServer2 Thrift interface when hive.server2.transport.mode is 'binary'.</description>
  </property>
```
listen_addresses = 'team-18-nn'  
8. (hadoop:jn) Скопируем env файл из теймплейта

```cp apache-hive-4.0.1-bin/conf/hive-env.sh.template apache-hive-4.0.1-bin/conf/hive-env.sh```

9. (hadoop:jn) Добавим в конфиг переменные окружения

```
export HIVE_HOME=/home/hadoop/apache-hive-4.0.1-bin
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HIVE_AUX_JARS_PATH=$HIVE_HOME/lib/*
```

10. (team:nn) Устанавливаем Postgresql

```sudo apt install postgresql postgresql-contrib```

11. (team:nn) Переключаемся на пользователя postgres

```sudo -i -u postgres```

12. (postgres:nn) Создаем базу данных и пользователя для работы с ней

```psql```
```CREATE DATABASE metastore;```
```CREATE USER hive with password 'hive';```
```GRANT ALL PRIVILEGES ON DATABASE "metastore" to hive;```
```ALTER DATABASE metastore OWNER TO hive;```

13. (team:nn) Редактируем конфиг постреса, заменим значение listen_addresses

```sudo vim /etc/postgresql/16/main/postgresql.conf```

```listen_addresses = 'team-18-nn'```     

14. (team:nn) Редактируем конфиг постреса, добавим IPv4 local connections (разрешим доступ только с jn)

```
sudo vim /etc/postgresql/16/main/pg_hba.conf
```

```
IPv4 local connections 
host    metastore             hive             192.168.1.74/32            password
```

15. (team:nn) Перезапускаем postgres

```
sudo systemctl restart postgresql
```

15. (team:nn) Перезапускаем postgres
```
sudo apt install postgresql
```

16. (team:jn) Устанавливаем клиент postgres

```
sudo apt install postgresql-client-16
```

17. (hadoop:jn) Скачиваем драйвер postgresql

``cd apache-hive-4.0.1-bin/lib``
```wget https://jdbc.postgresql.org/download/postgresql-42.7.4.jar```

18. (hadoop:jn) Добавить переменные окруженния в ~/.profile

```
export HADOOP_HOME=/home/hadoop/hadoop-3.4.0
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HIVE_HOME=/home/hadoop/apache-hive-4.0.1-bin
export HIVE_CONF_DIR=$HIVE_HOME/conf
export HIVE_AUX_JARS_PATH=$HIVE_HOME/lib/*
export PATH=$PATH:$HIVE_HOME/bin
```

19. (hadoop:jn) Инициализировать схему

```apache-hive-4.0.1-bin/bin/schematool -dbType postgres -initSchema```

20. (hadoop:jn) Запускаем hiveserver2

```hive --hiveconf hive.server2.enable.doAs=false --hiveconf hive.secruty.authorization.enable=false --service hiveserver2 1>> /tmp/hs2.log 2>> /tmp/hs2.log &```
