from pydantic import BaseModel

class PiParams(BaseModel):
    seed: int
