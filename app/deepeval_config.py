import os
from deepeval.models import DeepEvalBaseLLM
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeJudge(DeepEvalBaseLLM):
    """Claude as the judge LLM for DeepEval metrics."""

    def __init__(self, model: str = "claude-sonnet-5"):
        self.model_name = model
        workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")

        headers = {}
        if workspace_id:
            headers["anthropic-workspace-id"] = workspace_id

        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            default_headers=headers,
        )

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        text_parts = [
            block.text for block in response.content if block.type == "text"
        ]
        return "\n".join(text_parts)

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return self.model_name