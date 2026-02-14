from __future__ import annotations

from pydantic import BaseModel, Field


class RunConfig(BaseModel):
    model: str = Field(default="gpt-4.1-mini")
    max_output_tokens: int = Field(default=400)
    temperature: float = Field(default=0.2)
    output_dir: str = Field(default="artifacts")
