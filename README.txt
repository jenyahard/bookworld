#BOOKWORLD

###Блог для авторов книг, где пользователи могу делиться своими книгами, смотреть продукты коллег и обмениваться комментариями.
###BOOKWORLD написан на Django

Установка:
1. Клонируйте репозиторий:
    git clone ....
2. В корневой директории проекта создайте виртуальное окружение:
    python -m venv venv
3. Активируйте виртуальное окружение:
    source venv/Scripts/activate
    source venv/bin/activate    
4. Обновить Pip если не обновлен:
    python -m pip install --upgrade pip
5. В активированном виртуальном окружении разверните фреймворк Django версии 3.2.16: 
    pip install Django==3.2.16
6. Установите зависимости:
    pip install -r requirements.txt
7. В bookworld/bookworld/settings.py укажите свою MySQL БД.

Разработчик: Маслюк Евгений
Telegram: jenyahard