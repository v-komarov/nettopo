# Построитель топологии сетевых устройств доступа

Зависимости:
```
python3.6 -m pip install redis
python3.6 -m pip install networkx

```

- **send2redis.py** Формирует данные в виде json структуры по графам агрегаций 
- **links.json** Пример данных связей между коммутаторами
- **aggregations.json** Пример данных по агрегаторам
- **conf.py** Конфигурационный файл
- **fresult.json** Пример файла результатов

**Порядок работы** 

1. Периодически (через crontab) формируется общий граф всех устройств
1. Общий граф разбивается на графы агрегаций
1. Запись в redis ip агрегатора как ключа и данных по агрегации в виде значения (json)
1. Запись в redis ip устройств доступа агрегации как ключей и ip адреса агрегатора как значения (json)
1. Вывод данных в файл (опционально)
