
---

# 🌌 NASA API to Kafka to MySQL

## 🚀 Описание

Этот проект создан для получения данных из NASA API, их публикации в Kafka и последующего сохранения в базе данных MySQL. Проект разделен на две основные части:

1. **API-приложение на Flask** - Получает данные с NASA API и отправляет их в соответствующие топики Kafka.
2. **Консюмеры Kafka** - Читают данные из Kafka и записывают их в базу данных MySQL.

## 🛠️ Установка

### 📋 Предварительные требования

- Python 3.12+
- MySQL Server
- Kafka и Zookeeper (можно использовать локальную установку или Docker)

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/NasaApiKafkaMySQL.git
cd NasaApiKafkaMySQL
```

### 2. Создание и активация виртуального окружения

```bash
python -m venv main_env
source main_env/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка базы данных MySQL

1. Подключитесь к MySQL и создайте базу данных:

   ```sql
   CREATE DATABASE nasa_data;
   USE nasa_data;
   ```

2. Создайте таблицы:

   ```sql
   CREATE TABLE apod (
       id INT AUTO_INCREMENT PRIMARY KEY,
       date DATE,
       title VARCHAR(255),
       explanation TEXT,
       url VARCHAR(255),
       copyright VARCHAR(255)
   );

   CREATE TABLE neo (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       close_approach_date DATE,
       estimated_diameter_min_km FLOAT,
       estimated_diameter_max_km FLOAT,
       velocity_km_per_hour FLOAT,
       miss_distance_km FLOAT
   );
   ```

### 5. Настройка Kafka

1. Убедитесь, что Kafka и Zookeeper запущены.
2. Создайте топики для данных APOD и NEO:

   ```bash
   kafka-topics.sh --create --topic nasa_apod_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   kafka-topics.sh --create --topic nasa_neo_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

## 🚶‍♂️ Использование

### 1. Запуск Flask приложения

Запустите Flask приложение для получения данных из NASA API и отправки их в Kafka:

```bash
python app.py
```

### 2. Запуск консюмеров

Запустите консюмеры, которые будут читать данные из Kafka и сохранять их в MySQL:

```bash
python kafka_consumers/apod_consumer.py
python kafka_consumers/neo_consumer.py
```

### 3. Проверка данных

Проверьте данные, сохраненные в базе данных MySQL:

```sql
SELECT * FROM apod;
SELECT * FROM neo;
```

## 🗂️ Структура проекта

```
NasaApiKafkaMySQL/
│
├── app.py                     # Flask приложение для получения данных из NASA API и публикации в Kafka
├── requirements.txt           # Список зависимостей проекта
├── kafka_producer/
│   ├── __init__.py
│   └── producer.py            # Код для работы с Kafka продюсером
│
├── kafka_consumers/
│   ├── __init__.py
│   ├── apod_consumer.py       # Консюмер для данных APOD
│   └── neo_consumer.py        # Консюмер для данных NEO
│
├── api_fetcher/
│   ├── __init__.py
│   ├── apod.py                # Получение данных APOD из NASA API
│   └── neo.py                 # Получение данных NEO из NASA API
└── README.md                  # Документация проекта
```

