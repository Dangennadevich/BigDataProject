## ДЗ - 4

### Linux
1. (jn:hadoop) Создаем папку для Spark и скачиваем архив 

```
mkdir hadoop-3.4.0/spark
cd hadoop-3.4.0/spark
```

```wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-without-hadoop.tgz```


2. (jn:hadoop) Распакуем архив

```tar -zxvf spark-3.5.3-bin-without-hadoop.tgz```

3. (jn:hadoop) Зададим переменные окружения

```
cd spark-3.5.3-bin-without-hadoop/
pwd >> /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop
```

```
export SPARK_HOME=/home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop
export PATH=$PATH:SPARK_HOME/bin
export SPARK_DIST_CLASSPATH=$SPARK_HOME/jars/*:$(hadoop classpath)
```

4. (jn:hadoop) Запускаем мастер-узел из /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop`

```sbin/start-master.sh```

```sbin/stop-master.sh```

5. (jn:hadoop) Запускаем рабочий узел

```sbin/start-worker.sh spark://team-18-jn:7077 -d /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop/worker -h team-18-jn```

sbin/stop-worker.sh

```sbin/start-worker.sh spark://team-18-nn:7077 -d /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop/worker -h team-18-nn```


6. (jn:hadoop) Загружаем данные в HDFS

```hdfs dfs -put customers-2000000.csv /input```

7. (jn:hadoop) Доустановим переменные окружения  

```
export HADOOP_CONF_DIR=/home/hadoop/hadoop-3.4.0/etc/hadoop
export YARN_CONF_DIR=/home/hadoop/hadoop-3.4.0/etc/hadoop
```


### Python

1. (jn:team) Днеобходимо установить вериуальное окружение для рабоы с Spark, доустановим пакет python3-venv

```
sudo apt update
sudo apt install python3.12-venv
```

2. (jn:team) Создадим и входим в виртуальное окружение

```
python3 -m venv venv
```

3. (venv jn:hadoop) Добавим переменные окружения venv/bin/activate

При помощи команды из корня

```nano venv/bin/activate```

Добавим переменные

```
export HADOOP_CONF_DIR=/home/hadoop/hadoop-3.4.0/etc/hadoop
export YARN_CONF_DIR=/home/hadoop/hadoop-3.4.0/etc/hadoop
```

4. (venv jn:hadoop) Войдем в виртуальное окружение и установим необходимые библиотеки

```
source venv/bin/activate

pip install pyspark
pip install onetl
```

4. (venv jn:hadoop) Переходим в режим интерактивной оболочки и импортируем несколько библиотек

```python3```

```


select min(website), max(website), count(distinct website) from project.customers;