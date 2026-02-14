from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PromptCase(BaseModel):
    id: str
    category: str
    prompt: str
    notes: Optional[str] = None
    expect: Optional[Dict[str, Any]] = None  # lightweight expectations (keywords, refusal, json, etc.)


class PromptSuite(BaseModel):
    name: str
    description: str = ""
    cases: List[PromptCase] = Field(default_factory=list)


class RunResult(BaseModel):
    run_id: str
    case_id: str
    category: str
    model: str
    input_prompt: str
    output_text: str
    flags: Dict[str, Any]
    score: Dict[str, Any]
