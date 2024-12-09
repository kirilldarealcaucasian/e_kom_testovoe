## Как запустить:
1. git clone https://github.com/kirilldarealcaucasian/e_kom_testovoe.git
2. docker build -t testovoe .
3. docker run -p 8000:8000 testovoe
4. http://0.0.0.0:8000/docs - документация
при запуске приложения произойдет заполнение базы данных тестовыми данными.
для проверки корректности работы можно запустить internal/tests.py.   Для этого нужно узнать id контейнера
через docker ps, далее docker exec -it  <container_id> bash, потом python ./internal/tests.py