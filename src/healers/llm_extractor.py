import json
from typing import Any, Dict

from google import genai
from google.genai import types
from dotenv import load_dotenv

# Force the environment variables to load from the .env file
load_dotenv()

# The new Client automatically looks for the GEMINI_API_KEY environment variable
client = genai.Client()


class AIHealer:
    @staticmethod
    def extract_json(raw_html: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forces Gemini to extract structured data from raw HTML based on a dynamic schema.
        """
        print("[Healer] Engaging Gemini API (New SDK) for deterministic extraction...")

        safe_html = raw_html[:15000]

        prompt = f"""
        You are a strict data extraction engine. Extract the information from the RAW HTML
        and map it exactly to the keys in the TARGET SCHEMA.

        TARGET SCHEMA:
        {json.dumps(target_schema, indent=2)}

        RAW HTML:
        {safe_html}
        """

        try:
            # We use the updated 2.5-flash model via the new generate_content API
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0,  # Zero creativity, purely deterministic
                ),
            )

            # Parse the string response back into a Python Dictionary
            extracted_data = json.loads(response.text)
            return extracted_data

        except Exception as e:
            raise RuntimeError(f"Gemini Extraction failed: {str(e)}")
