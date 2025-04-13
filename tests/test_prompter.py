from struktcore_lite.core.prompter import build_prompt

def test_prompt_structure():
    prompt = build_prompt("Hello")
    assert isinstance(prompt, str)
    assert "User: Hello" in prompt
    assert "AI:" in prompt
