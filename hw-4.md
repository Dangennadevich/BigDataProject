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
pwd >> /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop```
```
export SPARK_HOME=/home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop
export PATH=$PATH:SPARK_HOME/bin
export SPARK_DIST_CLASSPATH=$SPARK_HOME/jars/*:$(hadoop classpath)
```
4. (jn:hadoop) Запускаем мастер-узел из /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop`

```sbin/start-master.sh```

5. Запускаем рабочий узел

```sbin/start-worker.sh spark://team-18-jn:7077 -d /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop/worker -h team-18-jn```




### Python

1. (jn:team) Днеобходимо установить вериуальное окружение для рабоы с Spark, доустановим пакет python3-venv

```
sudo apt update
sudo apt install python3.12-venv
```
2. (jn:hadoop) Создадим и входим в виртуальное окружение

```
python3 -m venv venv
source venv/bin/activate
```

3. (venv jn:hadoop) Установим необходимые библиотеки

```
pip install pyspark
pip install onetl
```