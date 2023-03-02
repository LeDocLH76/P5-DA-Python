OpenClassRooms student project
Course: Développement d’une application avec Python
Project: P5 Créez une API sécurisée RESTful en utilisant Django REST

step by step > to be completed

Gitclone

`python -m venv .env`

`.\.env\Scripts\activate`

`python -m pip install -r requirements.txt`

copy .env in config

`python manage.py migrate`

`python manage.py build_groups`

`python manage.py loaddata db-short.json`

`python manage.py runserver`

database state after populate

|        |         | Username |   User1    |   User2    |   User3    |   User4    |   User5    |   User6    |
| :----: | :-----: | :------: | :--------: | :--------: | :--------: | :--------: | :--------: | :--------: |
|        |         | User_PW  | user-pass1 | user-pass2 | user-pass3 | user-pass4 | user-pass5 | user-pass6 |
|        |         | User_ID  |     1      |     3      |     4      |     5      |     6      |     7      |
| Prj_ID |  Name   |   Type   |            |            |            |            |            |            |
|   1    | Prj_1_1 |    BE    |     OW     |     CO     |            |            |     CO     |            |
|   2    | Prj_1_2 |    FE    |     OW     |     CO     |     CO     |            |            |            |
|   3    | Prj_1_3 |    AD    |     OW     |     CO     |     CO     |     CO     |            |            |
|   4    | Prj_1_4 |    IO    |     OW     |            |     CO     |     CO     |     CO     |            |
|   5    | Prj_1_5 |    BE    |     OW     |            |            |     CO     |     CO     |            |
|   6    | Prj_2_1 |    FE    |            |     OW     |     CO     |            |            |            |
|   7    | Prj_2_2 |    AD    |            |     OW     |     CO     |     CO     |            |            |
|   8    | Prj_2_3 |    IO    |            |     OW     |            |     CO     |     CO     |            |
|   9    | Prj_2_4 |    BE    |            |     OW     |            |            |     CO     |            |
|   10   | Prj_2_5 |    FE    |            |     OW     |            |            |            |            |
|   11   | Prj_3_1 |    AD    |            |            |     OW     |     CO     |            |            |
|   12   | Prj_3_2 |    IO    |            |            |     OW     |            |     CO     |            |
|   13   | Prj_3_3 |    BE    |     CO     |            |     OW     |            |            |            |
|   14   | Prj_3_4 |    FE    |            |     CO     |     OW     |            |            |            |
|   15   | Prj_3_5 |    AD    |            |            |     OW     |            |            |            |
|   16   | Prj_4_1 |    IO    |            |            |     CO     |     OW     |            |            |
|   17   | Prj_4_2 |    BE    |            |     CO     |     CO     |     OW     |            |            |
|   18   | Prj_4_4 |    AD    |     CO     |     CO     |            |     OW     |            |            |
|   19   | Prj_4_5 |    IO    |     CO     |            |            |     OW     |            |            |
|   20   | Prj_5_1 |    BE    |            |            |            |     CO     |     OW     |            |
|   21   | Prj_5_2 |    FE    |            |            |     CO     |     CO     |     OW     |            |
|   22   | Prj_5_2 |    AD    |            |     CO     |     CO     |            |     OW     |            |
|   23   | Prj_5_4 |    IO    |     CO     |     CO     |            |            |     OW     |            |
|   24   | Prj_5_5 |    BE    |     CO     |            |            |            |     OW     |            |

Postman API documentation is [here] (https://documenter.getpostman.com/view/20281154/2s93CRJBAw)
