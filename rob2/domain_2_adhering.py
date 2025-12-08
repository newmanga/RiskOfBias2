# ============================================
# RoB 2.0 – Domain 2: Effect of Adhering to Intervention
# ============================================

from .common import DomainResult, NO, NO_INFO, Response, YES
from .questions import DOMAIN2_ADHERENCE_QUESTIONS


class Domain2AdherenceResult(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 2: Risk of Bias – Effect of Adhering to Intervention",
            judgement,
            explanation,
            path,
        )


# --------------------------------------------
# Returns next question code for adherence domain
# --------------------------------------------
def get_next_question_domain2_adhering(state: dict):
    """
    Given a state dict like:
        {"2.1": Response or None, ..., "2.6": Response or None}

    Returns:
        "2.x"  → next signalling question to answer
        None   → all questions answered
    """

    # Q2.1 – Deviations due to trial context
    if state.get("2.1") is None:
        return "2.1"

    # Q2.2 – Were deviations likely to affect outcome?
    if state.get("2.2") is None:
        return "2.2"

    aware = (state["2.1"] in (YES | NO_INFO)) or (state["2.2"] in (YES | NO_INFO))

    # Q2.3 – Non-protocol interventions balanced (only if awareness)
    if aware and state.get("2.3") is None:
        return "2.3"

    # Q2.4 – Failures in implementing the intervention
    if state.get("2.4") is None:
        return "2.4"

    # Q2.5 – Non-adherence that could affect outcomes
    if state.get("2.5") is None:
        return "2.5"

    # Q2.6 – Analysis appropriateness, conditional per template
    needs_analysis = (
        (state.get("2.3") in (NO | NO_INFO)) or
        (state["2.4"] in (YES | NO_INFO)) or
        (state["2.5"] in (YES | NO_INFO))
    )
    if needs_analysis and state.get("2.6") is None:
        return "2.6"

    # Done
    return None


# --------------------------------------------
# Final Risk of Bias Algorithm for Adhering-to-Intervention
# --------------------------------------------
def rob2_domain2_adhering(q2_1, q2_2, q2_3, q2_4, q2_5, q2_6):
    """
    Executes the full RoB 2 decision tree for Domain 2 (effect of adhering).
    """

    # Validate inputs
    for q in (q2_1, q2_2, q2_3, q2_4, q2_5, q2_6):
        if q is not None and not isinstance(q, Response):
            raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

    path = []

    # ------------------------------------------------------
    # HIGH RISK RULES
    # ------------------------------------------------------

    # Deviations occurred AND were likely to affect the outcome
    if q2_1 in YES and q2_2 in YES:
        path.append("Deviations arose due to trial context and were likely to affect outcomes → High risk.")
        return Domain2AdherenceResult(
            "High",
            "Outcome likely biased because deviations from intended intervention influenced results.",
            path,
        )

    # Deviations not balanced between groups
    if q2_1 in YES and q2_3 in NO:
        path.append("Deviations occurred and were not balanced between intervention groups → High risk.")
        return Domain2AdherenceResult(
            "High",
            "Bias likely introduced by imbalance in deviations across groups.",
            path,
        )

    # Inappropriate analysis AND likely biased
    if q2_5 in NO and q2_6 in YES:
        path.append("Inappropriate adherence-effect analysis and result likely biased → High risk.")
        return Domain2AdherenceResult(
            "High",
            "The adherence-effect estimate is likely biased due to inappropriate analysis.",
            path,
        )

    # ------------------------------------------------------
    # LOW RISK RULES
    # ------------------------------------------------------

    # No concerning deviations + adherence good + appropriate analysis
    if (q2_1 in (NO | NO_INFO)) and (q2_4 in YES | NO_INFO) and (q2_5 in YES | NO_INFO):
        path.append("No concerning deviations + adequate adherence + appropriate analysis → Low risk.")
        return Domain2AdherenceResult(
            "Low",
            "Bias unlikely since deviations did not meaningfully distort the adherence-based effect estimate.",
            path,
        )

    # ------------------------------------------------------
    # SOME CONCERNS
    # ------------------------------------------------------
    path.append(
        "No high-risk criteria met, but insufficient information to confirm low risk → Some concerns."
    )
    return Domain2AdherenceResult(
        "Some concerns",
        "Some uncertainty remains about deviations, adherence levels, or the appropriateness of the analysis.",
        path,
    )
