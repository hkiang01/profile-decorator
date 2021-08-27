from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """[summary]

    Returns
    -------
    str
        [description]
    """
    return {"Hello": "World"}
