# Это проект Yamdb 
 
[Ссылка на проект](http://51.250.4.170/api/v1/ "---")

## Здесь краткое описание проекта: 
    
#### проект состоит из трех частей:
    db - база данных Postgresql
    web - само приложение
    nginx - прокси сервер 

### Команды для запуска проектиа:
    docker-compose up
    docker comtainer ls
    docker exec -it XXXX bash (XXXX - первые цифры CONTAINER ID)
    python3 manage.py migrate
    
### Команда для создания суперпользователя:
    python3 manage.py createsuperuser

### Команда для заполнения базы начальными данными:
    python3 manage.py dumpdata > fixtures.json

![workflow](https://github.com/bobrolevv/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)