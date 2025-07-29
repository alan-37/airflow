# Пайплайн предсказания цен на автомобили с использованием Airflow и Docker

Этот проект реализует пайплайн машинного обучения для предсказания цен на автомобили с использованием Apache Airflow для оркестрации задач и Docker для контейнеризации среды.

## Структура проекта
```
airflow_hw/
├── docker-compose.yml # Конфигурация Docker
├── .env # Переменные окружения
├── data/
│   ├── models/ # Обученные модели (в формате pickle)
│   ├── predictions/ # Результаты предсказаний
│   ├── train/ # Обучающие данные
│   └── test/ # Тестовые данные (в формате JSON)
├── modules/
│   ├── pipeline.py # Пайплайн обучения модели
│   └── predict.py # Генерация предсказаний
└── dags/
    └── hw_dag.py # Определение DAG в Airflow
```


## Предварительные требования

- Docker Desktop
- Python 3.7+
- Git Bash (рекомендуется для Windows)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-логин/car-price-prediction.git
cd car-price-prediction
```

### 2. Настройка Docker
1. Скачайте официальный файл конфигурации Airflow
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
```
2. Отредактируйте файл docker-compose.yml
```yaml
volumes:
  - ${AIRFLOW_PROJ_DIR:-.}:/opt/airflow
```
3. Создайте файл .env:
```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

### 3. Инициализация Airflow

```bash
docker-compose up airflow-init
```

### 4. Запуск Airflow
```bash
docker-compose up -d
```

### 5. Доступ к интерфейсу Airflow
Откройте в браузере http://localhost:8080 (логин: airflow, пароль: airflow)

### 6. Запуск пайплайна
1. Активируйте DAG car_price_prediction в интерфейсе Airflow
2. Пайплайн выполнит следующие действия:
- Обучит модели на обучающих данных
- Выберет лучшую модель
- Сгенерирует предсказания для тестовых данных
- Сохранит результаты в папку data/predictions/

## Детали пайплайна
### Обучение модели (pipeline.py)
1. Предобработка данных:
   - Удаление ненужных колонок
   -  Обработка выбросов методом IQR
   - Создание новых признаков (short_model, age_category)
2. Обучение моделей:
   - Тестирование 3 моделей (Логистическая регрессия, Случайный лес, SVM)
   - Использование 4-кратной кросс-валидации
   - Выбор лучшей модели по метрике accuracy
   - Сохранение модели с временной меткой

### Генерация предсказаний (predict.py)
1. Загрузка последней обученной модели
2. Обработка всех JSON-файлов в папке data/test/
3. Генерация предсказаний
4. Сохранение результатов в CSV-файл в папке data/predictions/