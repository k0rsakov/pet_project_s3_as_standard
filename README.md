# pet_project_s3_as_standart
pet_project_s3_as_standart


## Создание виртуального окружения

```bash
python3.12 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install poetry && \
poetry lock && \
poetry install
```


## Разворачивание инфраструктуры

```bash
docker-compose up -d
```