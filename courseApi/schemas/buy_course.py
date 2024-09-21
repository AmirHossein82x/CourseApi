from pydantic import BaseModel


class CourseBoughtCreate(BaseModel):
    course_id: int
    payed:int