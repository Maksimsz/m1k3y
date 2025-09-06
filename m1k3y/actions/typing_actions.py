from ..injection.keyboard import type_text

def inject_text(text: str):
    type_text(text)
    return f"Typed {len(text)} characters."