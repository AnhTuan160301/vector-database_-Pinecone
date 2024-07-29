from pydantic import BaseModel


class SearchQueryInput(BaseModel):
    text: str


class SearchQueryOutput(BaseModel):
    input: str
    output: str
    intermediate_steps: list[str]
