from collections import deque

class ConversationContext:
    def __init__(self, max_len=10):
        self.messages = deque(maxlen=max_len)

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def to_prompt(self):
        return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in self.messages)