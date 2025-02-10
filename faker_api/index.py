from fastapi import FastAPI, HTTPException
from faker import Faker
from pydantic import BaseModel
import uvicorn

app = FastAPI()
fake = Faker()

data = []
id = 1

class User(BaseModel):
    user_id : int
    name : str
    email : str
    adress : str
    phone_number : str

@app.post("/generate")
def post_data():
    global id

    if id >= 10:
        raise HTTPException(status_code=400, detail="You cannot generate more than 10 users")

    try:
        user = User(
            user_id = id,
            name = fake.name(),
            email = fake.email(),
            adress = fake.street_address(),
            phone_number = fake.phone_number()
        )
        data.append(user)
        id+=1
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating data")

@app.get("/data")
def get_data():
    if not data:
        return {"Error" : "Data is empty"}

    return data

@app.delete("/delete/{user_id}")
def delete_data(user_id : int):
    user_to_delete = next((user for user in data if user.user_id == user_id), None)
    if user_to_delete:
        data.remove(user_to_delete)
        return {"User was successfully deleted" : user_to_delete}

    raise HTTPException(status_code=404, detail="User not found")



if __name__ == "__main__":
    uvicorn.run(app, port=5329)