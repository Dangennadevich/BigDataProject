## ДЗ - 5

0. Задача по трансформации данных из HDFS в ручном режиме выполнена в ДЗ-4 (скрипт `hw-4.py`):

- Переименованы поля
- Создано новое поле
- Применена группировка с агрегацией
- Применена сортировка
- Датафрейм репартицирован
- Датафрейм сохранен как таблица `'project.final_agg_datamart'` с партицированием по дате `'business_month'`

1. (local terminal -> hadoop:jn) Подключение с прокидыванием портов для UI Prefect и прочего

```
ssh -L 9870:176.109.91.20:9870 -L 19888:176.109.91.20:19888 -L 8088:176.109.91.20:8088 -L 10002:176.109.91.20:10002 -L 4200:176.109.91.20:4200 team@176.109.91.20
```
```
sudo -i -u hadoop
```

1. (jn:hadoop) Устанавливаем Prefect

- Переключаемся на наш venv
```
source venv/bin/activate
```
- (venv) Инициализируем установку Prefect через pip
```
pip install prefect
pip install prefect-schedules
```

2. Пишем скрипт для запуска процесса ETL с помощью Prefect и запускаем его

- (localhost) Скопируем скрипт с локального хоста
```
scp hw-5_manual.py team@176.109.91.20:/home/hadoop
```
- (venv) (jn:hadoop) Запустим скрипт и будем монитроить вывод
```
python3 hw-5_manual.py
```

3. Теперь нам нужно развернуть экземпляр Prefect, чтобы запустить скрипт на расписание

- (jn:hadoop) Создадим директорию для проектов Prefect
```
mkdir ~/prefect
```
- Создаем work-pool для автоматизации prefect
```
prefect work-pool create "default" --type "process"
```
- (venv) (jn:hadoop) Экспортируем переменную PREFECT_HOME и PREFECT_DEFAULT_WORK_POOL_NAME
```
export PREFECT_HOME=~/prefect
export PREFECT_DEFAULT_WORK_POOL_NAME="default"
export PREFECT_API_URL=http://176.109.91.20:4200/api
```
- Запустим worker для Prefect
```
prefect worker start --pool "default"
```
- Запустим сервер Prefect и можем открыть его UI `http://localhost:4200/flows` на локальной тачке, так как порты были проброшены
```
prefect server start --host 176.109.91.20
```
- Создадим директорию для хранения данных о потоках
```
mkdir ~/prefect/flows
```
- Скопируем скрипт `hw-5_deploy.py` в новую директорию
```
cp hw-5_deploy.py prefect/
```
- Запустим скрипт для создания деплоя
```
python3 prefect/hw-5_deploy.py
```
- Можем наслаждаться в UI Prefect как бегут таски и каждые пять минут сохраняется табличка с обработанными данными :)
