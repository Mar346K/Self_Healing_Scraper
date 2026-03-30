from src.healers.llm_extractor import AIHealer


# We use the built-in monkeypatch fixture to mock the Gemini API call
def test_extract_and_learn_parses_json_correctly(monkeypatch):
    # 1. Setup our fake target schema and HTML
    schema = {"price": "string"}
    fake_html = "<html><body><div id='price'>$45.00</div></body></html>"

    # 2. Create a fake response that mimics what Gemini 2.5 Flash would return
    class MockResponse:
        text = '{"extracted_data": {"price": "$45.00"}, "extraction_rules": {"price": "#price"}}'

    class MockModels:
        def generate_content(self, *args, **kwargs):
            return MockResponse()

    class MockClient:
        models = MockModels()

    # 3. Intercept the real client and replace it with our fake one
    monkeypatch.setattr("src.healers.llm_extractor.client", MockClient())

    # 4. Execute the test
    result = AIHealer.extract_and_learn(fake_html, schema)

    # 5. Assert the internal logic handled the payload correctly
    assert result["extracted_data"]["price"] == "$45.00"
    assert result["extraction_rules"]["price"] == "#price"
