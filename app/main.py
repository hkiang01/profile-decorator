from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root(thing: int):
    """[summary]

    Parameters
    ----------
    thing : str
        [description]

    Returns
    -------
    str
        [description]
    """
    return {"Hello": "World"}
