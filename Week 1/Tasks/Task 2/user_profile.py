
import re
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
    ValidationError,
    ConfigDict,
)


class UserProfile(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=2,
        max_length=100,
        description="User's full name"
    )

    age: int = Field(
        ge=18,
        le=120,
        description="Age must be between 18 and 120"
    )

    email: EmailStr

    pan: str = Field(
        description="Valid Indian PAN number"
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
            raise ValueError(
                "Name must contain only letters, spaces, "
                "periods, apostrophes, or hyphens"
            )
        return value

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, value: str) -> str:
        value = value.strip().upper()

        # Standard PAN structure: 5 letters, 4 digits, 1 letter
        if not re.fullmatch(
            r"[A-Z]{5}[0-9]{4}[A-Z]", value
        ):
            raise ValueError(
                "PAN must follow the format ABCDE1234F"
            )

        return value


# Test 1: Valid user profile
print("\nTesting data 1")
try:
    user = UserProfile(
        name="Harsh Kumar",
        age=24,
        email="harsh@example.com",
        pan="ABCDE1234F"
    )

    print("Valid profile created successfully!")
    print(user.model_dump())

except ValidationError as e:
    print("Validation failed:")
    print(e)


# Test 2: Invalid user profile
print("\nTesting data 2")
print("\nTesting invalid data...")

try:
    invalid_user = UserProfile(
        name="Harsh",
        age=55,
        email="harshmail.com",
        pan="ALE4231A"
    )

    print(invalid_user.model_dump())

except ValidationError as e:
    print("Validation errors detected:")
    for error in e.errors():
        field = ".".join(str(x) for x in error["loc"])
        print(f"- Field: {field}")
        print(f"  Error: {error['msg']}")
