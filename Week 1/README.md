# Week 1 - Python and Groq API Exercises

This folder contains three introductory Python exercises. They progress from
calling a language model, to validating data locally with Pydantic, to asking
a model for structured output that Pydantic validates.

## Project structure

- `Tasks/Task 1/test_groq.py` - Sends a prompt to the Groq chat completions API
  and prints the response.
- `Tasks/Task 2/user_profile.py` - Demonstrates Pydantic validation of a user
  profile, including name, age, email, and PAN-format checks. This script does
  not make an API request.
- `Tasks/Task 3/instructor_user.py` - Uses Groq and Instructor to request a
  fictional profile that conforms to a Pydantic model, then prints the
  validated result as JSON.

Each task is a standalone script. Run it from its task folder, and install
dependencies in the Python environment you use to run it.

## Requirements

- Python 3.10 or newer. Task 2 and Task 3 use modern Pydantic APIs.
- Internet access and a Groq API key for Task 1 and Task 3.
- Python packages for the task you want to run, listed in the corresponding
  section below.

## Configure the API key

Task 1 and Task 3 read the `GROQ_API_KEY` environment variable directly. They
do not load a `.env` file. In PowerShell, set the variable for the current
terminal session before running either API-backed task:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

The value is available to commands launched from that terminal. Open a new
PowerShell session and set it again when needed. Do not put the key in the
Python source, commit it to version control, or share it in screenshots or
messages. If the key is exposed, revoke it with Groq and create a replacement.

Task 2 only validates sample data locally; it does not require an API key.

## Task 1 - Call Groq and print a response

`Tasks/Task 1/test_groq.py` creates a Groq client, sends a request using the
`openai/gpt-oss-120b` model, and prints the response text. The example prompt
asks for a short explanation of artificial intelligence.

In PowerShell:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 1\Tasks\Task 1"
py -m pip install groq
$env:GROQ_API_KEY = "your_groq_api_key_here"
py test_groq.py
```

If the API key is not set, accessing `os.environ["GROQ_API_KEY"]` raises a
`KeyError`. A model-not-found or access error means the configured model may
not be available to the account or key being used.

## Task 2 - Validate a profile with Pydantic

`Tasks/Task 2/user_profile.py` defines a `UserProfile` model and runs two
examples: one profile intended to be valid and one intended to demonstrate
validation errors. It prints the valid model and reports the fields that fail
in the invalid example.

The schema checks:

- `name` is between 2 and 100 characters and contains only the characters
  permitted by the custom validator.
- `age` is an integer from 18 through 120.
- `email` is a valid email address.
- `pan` follows the structural pattern of five letters, four digits, and one
  letter. The validator converts it to uppercase before checking.

Run it with:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 1\Tasks\Task 2"
py -m pip install "pydantic[email]"
py user_profile.py
```

The PAN check verifies only the string's format; it does not establish that a
PAN is real, issued, or belongs to anyone. The sample profiles are for
demonstration and should not be used to identify a real person.

## Task 3 - Generate structured output with Instructor

`Tasks/Task 3/instructor_user.py` defines a Pydantic profile model, wraps a
Groq client with Instructor, and asks the model to generate a fictional Indian
adult profile. Instructor requests the result in the model's schema, and the
script prints the validated data as formatted JSON.

The name, age, email, and PAN are validated by Pydantic. The generated profile
is fictional test data; the PAN check verifies its format only and does not
verify that it is real or issued.

In PowerShell:

```powershell
Set-Location -LiteralPath "C:\Users\Harsh_Kumar\Desktop\GENAI'\Week 1\Tasks\Task 3"
py -m pip install groq instructor "pydantic[email]"
$env:GROQ_API_KEY = "your_groq_api_key_here"
py instructor_user.py
```

The script reports a clear error if `GROQ_API_KEY` is missing. If the API
request fails, it prints the error type and message.

## Troubleshooting

### `GROQ_API_KEY` is missing

Set it in the current PowerShell session before running Task 1 or Task 3:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

Check that you set the variable in the same terminal from which you launch
Python. Task 2 does not need this variable.

### `ModuleNotFoundError`

Install the package dependencies for the specific task. If you have multiple
Python installations or virtual environments, make sure the `py`/`python`
command used for installation matches the interpreter used to run the script.

### Email validation dependency is missing

Install Pydantic's email extra:

```powershell
py -m pip install "pydantic[email]"
```

### Groq returns a model or access error

Confirm the API key is correct and that the model `openai/gpt-oss-120b` is
available to your Groq account. Check the account's limits and internet
connection as well.

## Privacy and usage notes

- Task 1 prompts and Task 3 profile-generation requests are sent to Groq.
- Do not send real credentials, private user data, or real PAN information to
  the model.
- Task 3 explicitly requests fictional profile data. Its PAN validator checks
  syntax only; it is not an identity or tax-record verification.
- API usage may be subject to provider rate limits or charges.
