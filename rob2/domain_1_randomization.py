# ============================================
# RoB 2.0 – Domain 1: Randomization Process
# ============================================

from .common import DomainResult, NO, NO_INFO, Response, YES

# Domain 1 signalling questions
QUESTIONS = {
    "1.1": "Was the allocation sequence random?",
    "1.2": "Was the allocation sequence concealed until participants were enrolled and assigned?",
    "1.3": "Did baseline differences between groups suggest a problem with the randomization process?",
}


class Domain1Result(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 1: Risk of Bias – Randomization Process",
            judgement,
            explanation,
            path,
        )


# --------------------------------------------
# Return next signalling question code for Domain 1
# --------------------------------------------
def get_next_question_domain1(state: dict):
    """
    Domain 1 has 3 questions:
        1.1 – Sequence random?
        1.2 – Concealment adequate?
        1.3 – Baseline differences?

    Returns:
        "1.x" → next question to ask
        None  → all questions completed
    """

    if state.get("1.1") is None:
        return "1.1"

    if state.get("1.2") is None:
        return "1.2"

    if state.get("1.3") is None:
        return "1.3"

    return None


# --------------------------------------------
# Final Risk of Bias Algorithm for Domain 1
# (Based on the official RoB 2.0 decision tree)
# --------------------------------------------
def rob2_domain1(q1_1, q1_2, q1_3):
    """
    Computes final judgment for Domain 1.
    """

    # Validate inputs
    for q in (q1_1, q1_2, q1_3):
        if q is not None and not isinstance(q, Response):
            raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

    path = []

    # ------------------------------------------------------
    # HIGH RISK CONDITIONS
    # ------------------------------------------------------

    # 1.2 indicates allocation was NOT concealed
    if q1_2 in NO:
        path.append("1.2 = No/Probably No → Allocation NOT concealed → High risk.")
        return Domain1Result(
            "High",
            "The allocation sequence was not adequately concealed.",
            path,
        )

    # 1.1 indicates the sequence was not random
    if q1_1 in NO:
        path.append("1.1 = No/Probably No → Sequence not random → High risk.")
        return Domain1Result(
            "High",
            "The allocation sequence was not random or was predictable.",
            path,
        )

    # Baseline imbalance + concealment unknown
    if q1_3 in YES and q1_2 in NO_INFO:
        path.append("1.3 = Yes + 1.2 = No Information → Baseline imbalance + unknown concealment → High risk.")
        return Domain1Result(
            "High",
            "Significant baseline differences indicate problems, and concealment was not described.",
            path,
        )

    # Baseline imbalance + sequence non-random
    if q1_3 in YES and q1_1 in NO:
        path.append("1.3 = Yes + 1.1 = No → Imbalance + non-random sequence → High risk.")
        return Domain1Result(
            "High",
            "Baseline imbalance likely resulted from inadequate randomization.",
            path,
        )

    # ------------------------------------------------------
    # LOW RISK CONDITIONS
    # ------------------------------------------------------

    if q1_2 in YES and q1_3 in (NO | NO_INFO):
        if q1_1 in (YES | NO_INFO):
            path.append("1.2 = Yes → Allocation concealed.")
            path.append("1.3 = No/NI → No concerning baseline imbalance.")
            path.append("1.1 = Yes/NI → Random or plausibly random sequence.")
            return Domain1Result(
                "Low",
                "Randomization appears successful with no signs of bias.",
                path,
            )

    # ------------------------------------------------------
    # SOME CONCERNS
    # ------------------------------------------------------
    path.append(
        "No high-risk criteria met, but evidence is insufficient to confirm low risk → Some concerns."
    )

    return Domain1Result(
        "Some concerns",
        "Information is insufficient or ambiguous regarding randomization or concealment.",
        path,
    )
