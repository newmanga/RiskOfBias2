# ============================================
# RoB 2.0 – Domain 4: Measurement of the Outcome
# ============================================

from .common import DomainResult, NO, NO_INFO, Response, YES
from .questions import DOMAIN4_MEASUREMENT_QUESTIONS


class Domain4Result(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 4: Risk of Bias – Measurement of the Outcome",
            judgement,
            explanation,
            path,
        )


# --------------------------------------------
# Return next signalling question code for Domain 4
# --------------------------------------------
def get_next_question_domain4(state: dict):
    """
    Domain 4 question sequence:
        4.1 → 4.2 → 4.3 → 4.4

    Returns:
        "4.x" → next question
        None  → complete
    """

    if state.get("4.1") is None:
        return "4.1"

    if state.get("4.2") is None:
        return "4.2"

    if state.get("4.3") is None:
        return "4.3"

    if state.get("4.4") is None:
        return "4.4"

    return None


# --------------------------------------------
# Final Risk of Bias Algorithm for Domain 4
# --------------------------------------------
def rob2_domain4(q4_1, q4_2, q4_3, q4_4):
    """
    Executes the full RoB 2 decision tree for Domain 4 (Outcome Measurement).
    """

    # Validate inputs
    for q in (q4_1, q4_2, q4_3, q4_4):
        if q is not None and not isinstance(q, Response):
            raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

    path = []

    # ------------------------------------------------------
    # HIGH RISK RULES
    # ------------------------------------------------------

    # Awareness influencing outcome + likely affected
    if q4_3 in YES and q4_4 in YES:
        path.append("4.3 = Yes + 4.4 = Yes → Knowledge of intervention assignment likely influenced outcome assessment → High risk.")
        return Domain4Result(
            "High",
            "Outcome assessment was likely biased due to lack of blinding or subjective assessment.",
            path,
        )

    # Outcome measured differently between groups
    if q4_2 in NO:
        path.append("4.2 = No → Outcome measurement differed across intervention groups → High risk.")
        return Domain4Result(
            "High",
            "Outcome measurement methods differed between groups, introducing bias.",
            path,
        )

    # Measurement method inappropriate
    if q4_1 in NO:
        path.append("4.1 = No → Measurement method inappropriate → High risk.")
        return Domain4Result(
            "High",
            "Outcome measurement method was inappropriate for the construct of interest.",
            path,
        )

    # ------------------------------------------------------
    # LOW RISK RULES
    # ------------------------------------------------------

    if (
        q4_1 in YES and
        q4_2 in YES and
        (q4_3 in NO or q4_3 in NO_INFO) and
        (q4_4 in NO or q4_4 in NO_INFO)
    ):
        path.append("Appropriate measurement + similar across groups + no evidence assessor awareness influenced results → Low risk.")
        return Domain4Result(
            "Low",
            "Outcome measurement appears appropriate, consistent, and unlikely to be biased.",
            path,
        )

    # ------------------------------------------------------
    # SOME CONCERNS
    # ------------------------------------------------------
    path.append("Insufficient evidence for low risk, but high-risk conditions not met → Some concerns.")

    return Domain4Result(
        "Some concerns",
        "There is some uncertainty regarding potential influence on outcome measurement.",
        path,
    )
