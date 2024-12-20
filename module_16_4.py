from fastapi import FastAPI, Path
from fastapi import HTTPException
from pydantic import BaseModel
app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get("/users", response_model=list[User])
async def get_users() -> list[User]:
    return users

@app.post('/user/{username}/{age}', response_model=User)
async def user_post(username: str, age: int):
    if not users:
        user_id = 1
    else:
        user_id = users[-1].id          # Генерация ID
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)               # Добавление пользователя
    return new_user

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_users(user_id:int, username:str, age:int) ->User:
                # Обновляем данные пользователя
    if user_id != User(id=user_id):  # существует ли пользователь?
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = User(id=user_id, username=username, age=age)
    users[user_id - 1] = updated_user   # учитываем индексацию с 0
    return updated_user

@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int)-> User:
    if user_id != User(id=user_id):
        raise HTTPException(status_code=404, detail="User was not found")

    # Удаляем пользователя и возвращаем его
    deleted_user = users.pop(user_id - 1)
    return deleted_user



#   uvicorn module_16_4:app --reload
#   http://127.0.0.1:8000/users
#   http://127.0.0.1:8000/docs

