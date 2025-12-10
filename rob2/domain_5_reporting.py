# ============================================
# RoB 2.0 – Domain 5: Selection of the Reported Result
# ============================================

from .common import DomainResult, NO, NO_INFO, Response, YES

# Domain 5 signalling questions
QUESTIONS = {
    "5.1": "Were the data that produced this result analyzed according to a pre-specified analysis plan?",
    "5.2": "Were there multiple eligible outcome measurements (scales, definitions) within this outcome domain?",
    "5.3": "Were there multiple eligible analyses of the data?",
}


class Domain5Result(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 5: Risk of Bias – Selection of the Reported Result",
            judgement,
            explanation,
            path,
        )


# --------------------------------------------
# Return next signalling question code for Domain 5
# --------------------------------------------
def get_next_question_domain5(state: dict):
    """
    Domain 5 questions:
        5.1 → 5.2 → 5.3

    Returns:
        "5.x" → next question
        None  → complete
    """

    if state.get("5.1") is None:
        return "5.1"

    if state.get("5.2") is None:
        return "5.2"

    if state.get("5.3") is None:
        return "5.3"

    return None


# --------------------------------------------
# Final Risk of Bias Algorithm for Domain 5
# --------------------------------------------
def rob2_domain5(q5_1, q5_2, q5_3):
    """
    Executes the full RoB 2 decision tree for Domain 5 (Selective Reporting).
    """

    # Validate inputs
    for q in (q5_1, q5_2, q5_3):
        if q is not None and not isinstance(q, Response):
            raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

    path = []

    # ------------------------------------------------------
    # HIGH RISK RULES
    # ------------------------------------------------------

    # No pre-specified analysis plan AND multiple eligible measurements AND multiple eligible analyses
    if q5_1 in NO and q5_2 in YES and q5_3 in YES:
        path.append("5.1 = No + 5.2 = Yes + 5.3 = Yes → High risk of selective reporting.")
        return Domain5Result(
            "High",
            "Multiple outcome measurements and analyses were possible, and no pre-specified analysis plan existed.",
            path,
        )

    # ------------------------------------------------------
    # LOW RISK RULES
    # ------------------------------------------------------

    # Pre-specified analysis plan exists
    if q5_1 in YES:
        path.append("5.1 = Yes → Pre-specified analysis plan followed → Low risk.")
        return Domain5Result(
            "Low",
            "Results were analyzed according to a pre-specified analysis plan.",
            path,
        )

    # No multiplicity concerns
    if q5_2 in NO and q5_3 in NO:
        path.append("5.2 = No + 5.3 = No → No multiplicity concerns → Low risk.")
        return Domain5Result(
            "Low",
            "There were no multiple eligible outcome measurements or analyses.",
            path,
        )

    # ------------------------------------------------------
    # SOME CONCERNS
    # ------------------------------------------------------
    path.append("Not enough information for low risk, and high-risk conditions not met → Some concerns.")

    return Domain5Result(
        "Some concerns",
        "Potential selective reporting cannot be ruled out because of uncertainty about analysis choice or outcome selection.",
        path,
    )
