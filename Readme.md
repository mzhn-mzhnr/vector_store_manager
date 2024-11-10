# Сервис управления документами

Сервис позволяет загрузить, просмотреть и удалить документы

## :gear: Технологии

### Необходимое окружение

- ChromaDB
- [RAG-сервис](https://github.com/mzhn-mzhnr/ai)

### Стек:

- Python 3.12
- ChromaDB
- HuggingFace
- nltk

## :screwdriver: Конфигурация

Приложение настраивается при помощи переменных среды (Environment variables)

Пример конфигурации находиться в `example.env`
Выполните эту команду, чтобы скопировать пример

```bash
cp example.env .env
```

После чего отредактируйте файл `.env` в вашем текстовом редакторе

## :rocket: Развертывание

> [!Note]
> Обязательно настройте конфиг приложения. [Как это сделать?](#screwdriver-конфигурация)

`$ git clone git@github.com:mzhn-mzhnr/vector_store_manager.git`

`$ cd vector_store_manager`

`$ pip freeze -r requirements.txt`

`$ uvicorn vector_store_manager.main:app --host 0.0.0.0 --port 9000`
