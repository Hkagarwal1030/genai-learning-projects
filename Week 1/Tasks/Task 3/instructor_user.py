
import os
import re
import json
import instructor

from groq import Groq
from pydantic import BaseModel, Field, EmailStr, field_validator


# 1. Define the Pydantic schema
class UserProfile(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    age: int = Field(ge=18, le=120)
    email: EmailStr
    pan: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
            raise ValueError("Invalid name format")
        return value

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, value: str) -> str:
        value = value.strip().upper()
        if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", value):
            raise ValueError("Invalid PAN format")
        return value


# 2. Configure the Groq client
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Set it in your terminal first."
    )

groq_client = Groq(api_key=api_key)

client = instructor.from_groq(
    groq_client,
    mode=instructor.Mode.TOOLS
)


# 3. Request structured output from the cloud LLM
try:
    user = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        response_model=UserProfile,
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate fictional test profile data. "
                    "Return a plausible name, age, email, and "
                    "syntactically valid PAN. Do not claim the "
                    "PAN or email belongs to a real person."
                )
            },
            {
                "role": "user",
                "content": (
                    "Generate one fictional Indian adult user profile "
                    "for testing data validation."
                )
            }
        ],
    )

    # 4. Print the validated object as JSON
    print("Structured profile generated successfully!")
    print(user.model_dump_json(indent=2))

except Exception as e:
    print(f"Could not generate profile: {type(e).__name__}: {e}")
