import json
import os
from typing import Any, Dict

import google.generativeai as genai
from dotenv import load_dotenv

# Force the environment variables to load from the .env file
load_dotenv()

# Initialize the Gemini client
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


class AIHealer:
    @staticmethod
    def extract_json(raw_html: str, target_schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Forces Gemini to extract structured data from raw HTML based on a dynamic schema.
        """
        print("[Healer] Engaging Gemini API for deterministic extraction...")

        # Truncating for MVP speed, though Gemini has a massive 1M+ context window
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
            # We use the Flash model because it is blisteringly fast and practically free
            model = genai.GenerativeModel(
                "gemini-1.5-flash",
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.0,  # Zero creativity, purely deterministic
                },
            )

            response = model.generate_content(prompt)

            # Parse the string response back into a Python Dictionary
            extracted_data = json.loads(response.text)
            return extracted_data

        except Exception as e:
            raise RuntimeError(f"Gemini Extraction failed: {str(e)}")
