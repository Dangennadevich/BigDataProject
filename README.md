# BigDataProject

В проекте представлены инструкции по развертыванию таких компонентов BigData, как:
  *  Кластер hdfs включающий в себя 3 DataNode. Запущены и выполняются следующие демоны: NameNode, Secondary NameNode и три DataNode.
  *  Развернут YARN и опубликованы веб-интерфейсы основных и вспомогательных демонов для внешнего использования.
  *  Развернут Hive в конфигурации пригодной для производственной эксплуатации, т.е. с отдельным хранилищем метаданных.
  *  Трансформировать загруженные данные в таблицу Hive. Преобразовать полученную таблицу в партиционированную.
  *  Развертывание кластера Spark, работа с данными через Spark API
  *  Использование реализация регулярного процесса чтения, трансформации и записи данных под управлением оркестратора (Prefect)
  *  Работа с Greenplum (загрузка данных)
