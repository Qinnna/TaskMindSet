# TaskMindSet
## Загрузка представленных данных и визуализация
Изначально нам дан файл, содержащий 3 столбца: **"id события"**, **"ФИО участника события 1"**, **"ФИО участника события 2"**

Переименуем их в **"event_id"**, **"Full_name1"**, **"Full_name2"** для того, чтобы избежать конфликтов при считывании файла

После чего, посмотрим на данные и загрузим их в графовую БД. [Всё можно посмотреть в ноутбуке](https://colab.research.google.com/drive/149Q3hjCVU8AvaaLj5CVHISFW_JNj0tnT#scrollTo=137e444c)

Наконец, посмотрим, как выглядит граф в Neo4j Browser (***не полностью, ведь в виде png не получается загрузить***) ![graph](https://user-images.githubusercontent.com/74057520/222198640-18d008a0-9da9-46b4-8a65-0b409a363755.png)

>Интересных зависимостей мне найти не удалось: заметил только, что есть группы из *4* человек
***Найдем их, выполнив запрос:***
```Cypher
    MATCH (a:Person)<-[:common_event]-(b:Person)
    WITH a, count(b) as incomingNodes
    WHERE incomingNodes>1
    RETURN a
```
Получим
![graph_4](https://user-images.githubusercontent.com/74057520/222200446-19f4e03b-a87d-428f-9302-43b760a3a465.png)
## Создание rest сервиса на python к нашей БД
### Стек:
+ **IDE:** VS 2022
+ **Framework:** Flask
+ **Python:** 3.9
+ **[Необходимые версии библиотек указаны тут](https://github.com/Qinnna/TaskMindSet/blob/master/requirements.txt)**

Основная страница в итоге будет выглядить так ![index](https://user-images.githubusercontent.com/74057520/222203959-a1560297-11ce-440f-9c1b-c819c11f6a00.png)
Для демонстрации посмотрим еще на возможности получить людей из базы с общим id события и запросить свойства указанного человека![друзяшки](https://user-images.githubusercontent.com/74057520/222204841-a1be3015-c840-49fd-beee-14c88dbd15b7.png)
![свойства](https://user-images.githubusercontent.com/74057520/222204874-e8445b83-922b-42b0-a646-af2e518d733e.png)

Ну и просто представление всех людей из БД в JSON ![json](https://user-images.githubusercontent.com/74057520/222205029-089c9c31-49cb-4661-86dc-f89aca0c266e.png)


### P.S.
>В файле [cred.txt](https://github.com/Qinnna/TaskMindSet/blob/master/cred.txt) нужно указать логин и пароль к вашей БД Neo4j
