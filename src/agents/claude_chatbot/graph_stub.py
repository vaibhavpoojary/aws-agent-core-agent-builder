# Simple LangGraph-like stub
class SampleLangGraphAgent:
    def __init__(self):
        pass

    def greet(self, input_text: str):
        return f"Hello! You said: {input_text}"

    def farewell(self, input_text: str):
        return f"Goodbye! You said: {input_text}"

    def invoke(self, input_text: str):
        t = input_text.lower()
        if "hi" in t or "hello" in t:
            return self.greet(input_text)
        if "bye" in t or "goodbye" in t:
            return self.farewell(input_text)
        return f"Echo: {input_text}"
