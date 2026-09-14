import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeClient:
    """A simple wrapper around Claude API for testing."""

    def __init__(self, model: str = "claude-sonnet-5"):
        workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")

        custom_headers = {}
        if workspace_id:
            custom_headers["anthropic-workspace-id"] = workspace_id

        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            default_headers=custom_headers,
        )
        self.model = model

    def ask(self, prompt: str) -> str:
        """
        Send a prompt to Claude and return the response text.

        Raises:
            TypeError:  if prompt is not a string.
            ValueError: if prompt is empty or whitespace-only.
            RuntimeError: if the response contains no text block.
        """
        if not isinstance(prompt, str):
            raise TypeError(f"Prompt must be a string, got {type(prompt).__name__}")

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty or whitespace-only")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system="Answer concisely and directly. Do not add extra context unless explicitly asked.",
            messages=[{"role": "user", "content": prompt}],
        )

        text_parts = [
            block.text
            for block in response.content
            if block.type == "text"
        ]

        if not text_parts:
            raise RuntimeError(
                f"No text block in response. "
                f"Block types received: {[b.type for b in response.content]}"
            )

        return "\n".join(text_parts)