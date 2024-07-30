from pydantic import BaseModel


class SearchQueryInput(BaseModel):
    text: str


class SearchQueryOutput(BaseModel):
    input: str
    output: list[str]
