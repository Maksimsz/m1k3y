from m1k3y.nlp.parser import parse_llm_json

def test_parser_basic():
    raw = '{"intent":"chat","text":"Hello!"}'
    p = parse_llm_json(raw)
    assert p["intent"] == "chat"