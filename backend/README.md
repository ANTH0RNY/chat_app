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
|message/<int:id>| get | - | true | Returns all messages between current user and user of id given in url in descending order of time of structure: {"id": int, "to": int, "from":int, "date_created": datetime string, "body": string}|
|message/<int:id>|post| body: string| true | adds a message to db consisting of current user as sender and id as recipient|
| logout| get | - | true | revokes current token access token |
| chats | get | - | true | returns a list of users who have sent or received message from current user |
| add_message/<string:username> | post | body: string | true | sends a message from current user to user with username in the url |
| / | get | - | false | returns a greeting, used for test purposes to see if server is running |


___
## Populating the tables withfake values
**make sure your virtual environment is active**
Accessing flask shell
```shell
flask shell
```
**If doning for the first time** you may need to manually make the table
```python
from app import db
db.create_all()
```

importing functions, *assuming you are at root directory*
```python
from app.faker import make_users, make_messages
make_users() #to make users this should be first step assuming no user is already made
make_messages() #to make messages
```
General good practice to make much, much more messages than users

## Using socketIO
### server side
Enable socketio cors if not being servered from same url
If more than one url seperate with comma
```shell
export SOCKETIO_CORS=URL1,URL2,URL3
```
After successful connection the websocket will send a confirmation message to `echo`
___
### frontend
#### setting up
In the frontend you need the users jwt access token.
```js
import {io} from "socket.io-client";
const socket = io("http://127.0.0.1:5000", {auth:JSON.stringify({token:"Your token"})})
```
To confirm connection. It will console log `you have been connected`
```js
socket.on('echo', (data)=>{
  console.log(data)
})
```
To receive new messages when sent using websocket you listen on users username
```js
socket.on("username", (data)=>{
    // data is message sent from server
})
```