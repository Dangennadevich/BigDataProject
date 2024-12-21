## ДЗ - 4

0. Доработки

- (jn:team) Добавить в файл `/etc/hosts` alias хоста неймноды
    ```
    192.168.1.75 team-18-nn
    ```
- (nn,jn,dn00,dn01:hadoop) Отредактировать конфиг yarn в файле `~/hadoop-3.4.0/etc/hadoop/yarn-site.xml` (поменять/добавить property с адресом)
    ```
     <property>
            <name>yarn.resourcemanager.address</name>
            <value>team-18-nn:8032</value>
    </property>
    ```
- (jn:hadoop) Чтобы корректно работал spark, необходимо поставить другую версию Hive `apache-hive-4.0.0-alpha-2-bin.tar.gz` для этого можно проделать все те же шаги, что и в инструкции №3, заменяя пути на директорию с другой версией Hive


- (Локальный ПК) Файл с локального ПК (Новый датасет) загружаем на сервер, сам файл скачиваем тут: 
`https://drive.google.com/file/d/1lxJSvw__l9emIbJY_cLNBtJZrXgB3W7B/view?usp=share_link`

```scp customers-2000000.csv team@176.109.91.20```

- (jn:team) Копируем датасет для пользователя hadoop
```scp customers-2000000.csv hadoop@192.168.1.74```

1. (jn:hadoop) Создаем папку для Spark и скачиваем архив 

```
mkdir hadoop-3.4.0/spark
cd hadoop-3.4.0/spark
```
```
wget https://dlcdn.apache.org/spark/spark-3.5.3/spark-3.5.3-bin-without-hadoop.tgz
```

2. (jn:hadoop) Распакуем архив

```tar -zxvf spark-3.5.3-bin-without-hadoop.tgz```

3. (jn:hadoop) Зададим переменные окружения

```
cd spark-3.5.3-bin-without-hadoop/
pwd >> /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop```

export SPARK_HOME=/home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop
export PATH=$PATH:SPARK_HOME/bin
export SPARK_DIST_CLASSPATH=$SPARK_HOME/jars/*:$(hadoop classpath)
```

4. (jn:hadoop) Запускаем мастер-узел из /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop`

```sbin/start-master.sh```

```sbin/stop-master.sh```

5. (jn:hadoop) Запускаем рабочий узел

```sbin/start-worker.sh spark://team-18-jn:7077 -d /home/hadoop/hadoop-3.4.0/spark/spark-3.5.3-bin-without-hadoop/worker -h team-18-jn```

6. (jn:team) Необходимо установить вериуальное окружение для рабоы с Spark, доустановим пакет python3-venv

```
sudo apt update
sudo apt install python3.12-venv
```
7. (jn:hadoop) Создадим и входим в виртуальное окружение

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

8. (venv jn:hadoop) Установим необходимые библиотеки

```
pip install pyspark
pip install onetl
```

9. (localhost) Скопируем python скрипт hw-4.py

```
scp hw-4.py team@176.109.91.20:/home/hadoop
```

10. (venv jn:hadoop) Запустим скрипт и убедимся в корректности его работы, дождавшись вывода об успешном сохранении таблицы. 

```
python3 hw-4.py
```
