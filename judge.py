from deepeval.models.base_model import DeepEvalBaseLLM
from ollama import Client


class OllamaJudge(DeepEvalBaseLLM):

    def __init__(self):
        self.client = Client(
            host="http://localhost:11434"
        )

        self.model = "llama3.2:3b"

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        return response["message"]["content"]

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model


judge_model = OllamaJudge()