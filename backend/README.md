# Chat app backend
This is a flask backend for my chat app
## Getting Started
1. setting up virtual environment
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ```
2. installing dependancies
    ```shell
    pip install -r requirements.txt
    ```
3. exporting the app file
    ```shell
    export FLASK_APP=chat_app.py
    ```
4. running app
    ```shell
    flask run
    ```
## Routes

|end point|method|body|authentication|description|
|---|---|---|---|---|
|user| get |-|true|get current authenticated user details|
|user| post | username:string, password:string|false|Creates new user in database|
|login|post| username:string, password:string |false | returns access token for logining in|
|login|get| - |true| Revokes access token | 
|message/<int: id>| get | - | true | Returns all messages between current user and user of id given in url in descending order of time of structure: {"id": int, "to": int, "from":int, "date_created": datetime string, "body": string}|
|message/<int: id>|post| body: string| true | adds a message to db consisting of current user as sender and id as recipient|

___
## Populating the tables withfake values
**make sure your virtual environment is active**
Accessing flask shell
```shell
flask shell
```
importing functions, *assuming you are at root directory*
```python
from app.faker import make_users, make_messages
make_users() #to make users this should be first step assuming no user already in it
make_messages() #to make messages
```
General good practice to make much, much more messages than users