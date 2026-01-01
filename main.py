from fastapi import Body, FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello WOrld"}

@app.get("/getPost")
def get_post():
    return {"Data": "this is your posts"}

@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} content:{payload['content']} "}