import json
from typing import Any, Dict, cast

from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()


class AIHealer:
    @staticmethod
    def extract_and_learn(
        raw_html: str, target_schema: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Forces Gemini to extract data AND generate the CSS selectors needed to find it again.
        """
        print(
            "[Healer] Engaging Gemini API to extract data and write new extraction rules..."
        )

        safe_html = raw_html[:15000]

        prompt = f"""
        You are a strict data extraction and web scraping engineering assistant.

        You have two jobs:
        1. Extract the information from the RAW HTML and map it exactly to the keys in the TARGET SCHEMA.
        2. For every key in the TARGET SCHEMA, provide the most robust CSS selector that can be used to extract that specific data directly from the DOM using Playwright.

        You MUST return a JSON object with EXACTLY two top-level keys:
        - "extracted_data": containing the data matching the TARGET SCHEMA.
        - "extraction_rules": containing a dictionary mapping the same schema keys to their CSS selectors.

        TARGET SCHEMA:
        {json.dumps(target_schema, indent=2)}

        RAW HTML:
        {safe_html}
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json", temperature=0.0
                ),
            )

            # 1. Guard against None returns
            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            # 2. Cast the parsed JSON explicitly to a Dictionary
            payload = cast(Dict[str, Any], json.loads(response.text))
            return payload

        except Exception as e:
            raise RuntimeError(f"Gemini Extraction failed: {str(e)}")
