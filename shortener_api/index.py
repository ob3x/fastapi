from fastapi import FastAPI
import string
import random
import json
import uvicorn

app = FastAPI()

links = []
letters = string.ascii_lowercase + string.ascii_uppercase + string.digits


def send_to_datebase():
    with open("database.json", "w") as file:
        json.dump(links, file)

def check_database():
    with open("database.json", "r") as file:
        returned_links = json.load(file)
    return returned_links

def generate_short_link():
    link = []
    for _ in range(random.randint(6, 8)):
        random_letter = random.choice(letters)
        link.append(random_letter)

    short_link = "".join(link)
    return short_link

@app.post("/generate-url/")
def generate_url(user_link : str):
    short_link = generate_short_link()
    links.append({"url" : user_link, "short_url" : short_link})
    send_to_datebase()
    return {"Short Url" : short_link}

@app.get("/check-links/")
def check_links():
    links = check_database()
    return {"All Urls" : links}

@app.get("/use-link/")
def use_link(short_link: str):
    links = check_database()
    for element in links:
        if element["short_url"] == short_link:
            return {"Your url": element["url"]}
    
    return {"Error": "Link not found"}


if __name__ == "__main__":
    uvicorn.run(app)