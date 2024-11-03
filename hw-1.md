## ДЗ - 1

1. Создаем пользователя hadoop без прав sudo

```sudo adduser hadoop```

2. Переключаемся на этого пользователя

```sudo -i -u hadoop```

3. Cоздаем ssh ключ и сохраняем его публичную часть (заранее скопируем публичные ключи к себе локально для шага 5)

```ssh-keygen```

4. Повторяем п.1 - п.3 для каждой машины (nn, dn-00, dn-01)
Для этого от пользователя `team` по очереди подключаемся к каждой машине с jump node
```ssh team@192.168.1.75```
```ssh team@192.168.1.76```
```ssh team@192.168.1.77```

5. На jump node создаем файл, куда запишем все публичные shh ключи сгенерированный ранее

```touch .ssh/authorized_keys```
```nano .ssh/authorized_keys```

6. Копируем authorized_keys на каждую машину
Переключаемся на пользователя `hadoop`

```sudo -i -u hadoop```

```scp .ssh/authorized_keys hadoop@192.168.1.75:/home/hadoop/.ssh/authorized_keys```

```scp .ssh/authorized_keys hadoop@192.168.1.76:/home/hadoop/.ssh/authorized_keys```

```scp .ssh/authorized_keys hadoop@192.168.1.77:/home/hadoop/.ssh/authorized_keys```

7. Скачиваем дистрибутив Hadoop 3.4.0 на jump node

```wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0.tar.gz```

8. Отправляем дистрибутив на каждую машину

```scp hadoop-3.4.0.tar.gz hadoop@192.168.1.75:/home/hadoop/hadoop-3.4.0.tar.gz```

```scp hadoop-3.4.0.tar.gz hadoop@192.168.1.76:/home/hadoop/hadoop-3.4.0.tar.gz```

```scp hadoop-3.4.0.tar.gz hadoop@192.168.1.77:/home/hadoop/hadoop-3.4.0.tar.gz```
 

9. Разархивируем дистрибутив Hadoop 3.4.0 на всех нодах

```tar -xvzf hadoop-3.4.0.tar.gz```

10. На NameNode добавим переменные окружения в файл ~/.profile

```
export HADOOP_HOME=/home/hadoop/hadoop-3.4.0
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

11. Копируем profile на дата ноды

```scp ~/.profile hadoop@192.168.1.76:/home/hadoop/.profile```

```scp ~/.profile hadoop@192.168.1.77:/home/hadoop/.profile```

12. Активируем переменные командой

```source ~/.profile```

13. Добавим переменную окружения в файл hadoop-3.4.0/etc/hadoop/hadoop-env.sh на всех нодах

```JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64```

14. Скопируем отредактированный файл окружения на все дата ноды

```scp hadoop-3.4.0/etc/hadoop/hadoop-env.sh hadoop@192.168.1.76:/home/hadoop/hadoop-3.4.0/etc/hadoop/hadoop-env.sh```

```scp hadoop-3.4.0/etc/hadoop/hadoop-env.sh hadoop@192.168.1.77:/home/hadoop/hadoop-3.4.0/etc/hadoop/hadoop-env.sh```

15. Добавим property в конфигурационный файл NameNode `hadoop-3.4.0/etc/hadoop/core-site.xml`

```
<configuration>
        <property>
                <name>fs.defaultFS</name>
                <value>hdfs://team-18-nn:9000</value>
        </property>
</configuration>
```

16. Добавим property в конфигурационный файл NameNode `hadoop-3.4.0/etc/hadoop/hdfs-site.xml`

```
<configuration>
        <property>
                <name>dfs.replication</name>
                <value>3</value>
        </property>
</configuration>
```

17. Добавим хосты в конфигурационный файл NameNode `hadoop-3.4.0/etc/hadoop/workers`

```
team-18-nn
team-18-dn-00
team-18-dn-01
```

18. Добавим хосты в `/etc/hosts` под пользователем `team`

```sudo nano /etc/hosts```

для `team-18-nn`
```
192.168.1.76 team-18-dn-00
192.168.1.77 team-18-dn-01
```

для `team-18-dn-00`
```
192.168.1.75 team-18-nn
192.168.1.77 team-18-dn-01
```

для `team-18-dn-01`
```
192.168.1.75 team-18-nn
192.168.1.76 team-18-dn-00
```

18. Скопируем созданные файлы на дата ноды

```
scp hadoop-3.4.0/etc/hadoop/core-site.xml hadoop@192.168.1.76:/home/hadoop/hadoop-3.4.0/etc/hadoop/core-site.xml && \
scp hadoop-3.4.0/etc/hadoop/core-site.xml hadoop@192.168.1.77:/home/hadoop/hadoop-3.4.0/etc/hadoop/core-site.xml && \
scp hadoop-3.4.0/etc/hadoop/hdfs-site.xml hadoop@192.168.1.76:/home/hadoop/hadoop-3.4.0/etc/hadoop/hdfs-site.xml && \
scp hadoop-3.4.0/etc/hadoop/hdfs-site.xml hadoop@192.168.1.77:/home/hadoop/hadoop-3.4.0/etc/hadoop/hdfs-site.xml && \
scp hadoop-3.4.0/etc/hadoop/workers hadoop@192.168.1.76:/home/hadoop/hadoop-3.4.0/etc/hadoop/workers && \
scp hadoop-3.4.0/etc/hadoop/workers hadoop@192.168.1.77:/home/hadoop/hadoop-3.4.0/etc/hadoop/workers

```

18. Форматируем файловую систему NameNode

```
hadoop-3.4.0/bin/hdfs namenode -format
```

19. Запустим dfs

```hadoop-3.4.0/sbin/start-dfs.sh```
