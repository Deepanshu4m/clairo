import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

PARSE_PROMPT = """
You are a resume parsing expert. Given the raw text of a resume, extract the following information and return ONLY a valid JSON object with no explanation or markdown.

Schema:
{{
  "full_name": "string or null",
  "summary": "brief professional summary in 2-3 sentences or null",
  "skills": ["list", "of", "skills"],
  "experience": [
    {{
      "role": "Job Title",
      "company": "Company Name",
      "years": "duration e.g. 2019-2022 or 3 years"
    }}
  ],
  "education": [
    {{
      "degree": "Degree name",
      "institution": "University/College name",
      "year": "graduation year or range"
    }}
  ]
}}

Resume Text:
{resume_text}
"""

async def parse_resume(raw_text: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.2,
    )

    prompt = PARSE_PROMPT.format(resume_text=raw_text)
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    
    content = response.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    
    return json.loads(content.strip())