
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from pydantic import BaseModel

color_mapping = {
    "low": "blue",
    "medium": "orange",
    "high": "red"
}

emoji_mapping = {
    "low": "ℹ️",
    "medium": "⚠️",
    "high": "🚨"
}


class ResultSeverity(str, Enum):
    """Classifications for how severe a result can be."""

    low = "low"
    medium = "medium"
    high = "high"



    @property
    def color(self):
        return self.color_mapping[self]

class ResultColorMap(str, Enum):
    """Classifications for how severe a result can be."""

    low = "blue"
    medium = "orange"
    high = "red"

class EvaluatorViolation(BaseModel):
    """
    A single instance of a violation of a dbt project evaluator rule.
    """

    short_summary: str
    long_summary: str
    exceptions: Optional[str]
    model: str
    unique_id: str
    severity: ResultSeverity
    rule_set: str
    rule_name: str

    def __str__(self):
        return f":{color_mapping.get(self.severity.value)}[{emoji_mapping.get(self.severity.value)} - {self.model} - {self.rule_set} - {self.rule_name}]"