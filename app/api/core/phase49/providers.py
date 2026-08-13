from __future__ import annotations

from dataclasses import dataclass
import json
import os
from urllib.request import Request, urlopen


class ModelProvider:
    configured = False
    live = False

    def generate(self, *, system: str, prompt: str, model: str | None = None) -> str:
        raise RuntimeError("MODEL_PROVIDER_NOT_CONNECTED")


class OpenAICompatibleProvider(ModelProvider):
    configured = True
    live = True

    def __init__(self, api_key: str | None = None, base_url: str | None = None, default_model: str | None = None):
        self.api_key = api_key or os.getenv("MODEL_API_KEY")
        self.base_url = (base_url or os.getenv("MODEL_API_BASE") or "https://api.openai.com/v1").rstrip("/")
        self.default_model = default_model or os.getenv("MODEL_NAME")
        if not self.api_key or not self.default_model:
            raise RuntimeError("MODEL_CONFIGURATION_REQUIRED")

    def generate(self, *, system: str, prompt: str, model: str | None = None) -> str:
        payload = json.dumps({"model": model or self.default_model, "messages": [
            {"role": "system", "content": system}, {"role": "user", "content": prompt}], "temperature": 0.2}).encode()
        req = Request(f"{self.base_url}/chat/completions", data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Content-Type", "application/json")
        with urlopen(req, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
        return str(data["choices"][0]["message"]["content"])


@dataclass
class MockModelProvider(ModelProvider):
    response: str = "MOCKED_RESULT"
    configured: bool = True
    live: bool = False

    def generate(self, *, system: str, prompt: str, model: str | None = None) -> str:
        return self.response
