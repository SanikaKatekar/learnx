from pydantic import BaseModel

class RequestPayload(BaseModel):
    topic: str
    level: str
    metaphor_api_key: str
    openai_api_key: str

class ResponsePayload(BaseModel):
    StudyPlan: dict