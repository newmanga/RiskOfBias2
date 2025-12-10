"""Shared types and helpers for RoB domain evaluations."""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Iterable, List, Optional


class Response(Enum):
    Y = "Y"   # Yes
    PY = "PY"  # Probably Yes
    NI = "NI"  # No Information
    PN = "PN"  # Probably No
    N = "N"   # No


YES = {Response.Y, Response.PY}
NO = {Response.N, Response.PN}
NO_INFO = {Response.NI}


class DomainResult:
    """Container for final RoB judgement across domains."""

    def __init__(
        self,
        domain_name: str,
        judgement: str,
        explanation: str,
        path: Iterable[str],
    ):
        self.domain_name = domain_name
        self.judgement = judgement
        self.explanation = explanation
        self.path: List[str] = list(path)

    def pretty(self):
        print(f"=== {self.domain_name}: Risk of Bias ===")
        print("Final Judgement:", self.judgement)
        print("\n--- Decision Path ---")
        for step in self.path:
            print("•", step)
        print("\n--- Explanation ---")
        print(self.explanation)
        print("====================================================================")


@dataclass
class DomainSpec:
    """Metadata and hooks for a RoB domain."""

    key: str
    title: str
    questions: Dict[str, str]
    get_next_question: Callable[[dict], Optional[str]]
    evaluate: Callable[..., DomainResult]


class BaseDomain:
    """Common interface for domain implementations."""

    key: str
    title: str
    questions: Dict[str, str]

    def get_next_question(self, state: dict) -> Optional[str]:
        raise NotImplementedError

    def evaluate(self, *args, **kwargs) -> DomainResult:
        raise NotImplementedError

    def as_spec(self) -> DomainSpec:
        """Return a light registry-friendly view of this domain."""
        return DomainSpec(
            key=self.key,
            title=self.title,
            questions=self.questions,
            get_next_question=self.get_next_question,
            evaluate=self.evaluate,
        )
