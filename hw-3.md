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

Добавляем новое property в конец конфига
```
  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
    <description>Defines the rewrite policy, the valid values are those defined in RewritePolicy enum</description>
  </property>
```

