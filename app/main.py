from fastapi import FastAPI
from profile_decorator.profile_memory import profile_memory

app = FastAPI()


@app.get("/")
@profile_memory
def read_root():
    """[summary]

    Returns
    -------
    str
        [description]
    """
    return {"Hello": "World"}
