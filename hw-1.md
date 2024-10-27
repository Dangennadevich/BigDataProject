## ДЗ - 1

1. Создаем пользователя hadoop без прав sudo
```sudo adduser hadoop```

2. Переключаемся на этого пользователя

```sudo -i -u hadoop```

3. Cоздаем ssh ключ и сохраняем его публичную часть

```ssh-keygen```

4. Повторяем п.1 - п.3 для каждой машины (nn, dn-00, dn-01)

5. На jump node создаем файл, куда запишем все публичные shh ключи сгенерированный ранее

```.ssh/authorized_keys```

6. Копируем authorized_keys на каждую машину

```scp .ssh/authorized_keys hadoop@192.168.1.75:/home/hadoop/.ssh/authorized_keys```
```scp .ssh/authorized_keys hadoop@192.168.1.76:/home/hadoop/.ssh/authorized_keys```
```scp .ssh/authorized_keys hadoop@192.168.1.77:/home/hadoop/.ssh/authorized_keys```

7. Скачиваем дистрибутив Hadoop 3.4.0 на jump node

```wget https://dlcdn.apache.org/hadoop/common/hadoop-3.4.0/hadoop-3.4.0-src.tar.gz```

8. Отправляем дистрибутив на каждую машину

```scp hadoop-3.4.0-src.tar.gz hadoop@192.168.1.75:/home/hadoop/hadoop-3.4.0-src.tar.gz```
```scp hadoop-3.4.0-src.tar.gz hadoop@192.168.1.76:/home/hadoop/hadoop-3.4.0-src.tar.gz```
```scp hadoop-3.4.0-src.tar.gz hadoop@192.168.1.77:/home/hadoop/hadoop-3.4.0-src.tar.gz```
