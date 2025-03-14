from pydantic import BaseModel, field_validator


class AuthorDetail(BaseModel):
    id: int
    name: str


class AuthorCreate(BaseModel):
    name: str

    @field_validator("name", check_fields=False)
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Author name can't be empty.")
        return value
