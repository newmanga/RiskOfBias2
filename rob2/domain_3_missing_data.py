# ============================================
# RoB 2.0 – Domain 3: Missing Outcome Data
# ============================================

from .common import DomainResult, NO, NO_INFO, Response, YES

# Domain 3 signalling questions
QUESTIONS = {
    "3.1": "Were data for this outcome available for all or nearly all participants randomized?",
    "3.2": "If not, is there evidence that the result was not biased by missing outcome data?",
    "3.3": "Could the missingness depend on the true value of the outcome?",
    "3.4": "If yes, is the proportion of missing data not sufficient to induce clinically relevant bias?",
}


class Domain3Result(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 3: Risk of Bias – Missing Outcome Data",
            judgement,
            explanation,
            path,
        )


# --------------------------------------------
# Return next signalling question code for Domain 3
# --------------------------------------------
def get_next_question_domain3(state: dict):
    """
    Sequence:
      3.1 → 3.2 (if 3.1 = N/PN/NI) → 3.3 (if 3.2 = N/PN) → 3.4 (if 3.3 = Y/PY/NI)

    Returns:
        "3.x" → next question to ask
        None  → complete
    """

    if state.get("3.1") is None:
        return "3.1"

    if state.get("3.2") is None and state["3.1"] in (NO | NO_INFO):
        return "3.2"

    if state.get("3.3") is None and state.get("3.2") in NO:
        return "3.3"

    if state.get("3.4") is None and state.get("3.3") in (YES | NO_INFO):
        return "3.4"

    return None


# --------------------------------------------
# Final Risk of Bias Algorithm for Domain 3
# --------------------------------------------
def rob2_domain3(q3_1, q3_2, q3_3, q3_4):
    """
    Executes the full RoB 2 decision tree for Domain 3 (Missing Outcome Data).
    """

    # Validate inputs
    for q in (q3_1, q3_2, q3_3, q3_4):
        if q is not None and not isinstance(q, Response):
            raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

    path = []

    # ------------------------------------------------------
    # HIGH RISK RULES
    # ------------------------------------------------------

    # Missing data likely depends on true outcome → high risk
    if q3_3 in YES and q3_4 in NO:
        path.append("3.3 = Yes + 3.4 = No → Missingness likely depends on true outcome and proportion is concerning → High risk.")
        return Domain3Result(
            "High",
            "The amount and mechanism of missing outcome data are likely to bias results.",
            path,
        )

    # If not all/nearly all data are available AND no evidence missingness is not biasing
    if q3_1 in NO and q3_2 in NO:
        path.append("3.1 = No + 3.2 = No → Missing data not shown to be non-biased → High risk.")
        return Domain3Result(
            "High",
            "There is no reassurance that missing data did not bias the results.",
            path,
        )

    # ------------------------------------------------------
    # LOW RISK RULES
    # ------------------------------------------------------

    # Criterion 1: Nearly all data available
    if q3_1 in YES:
        path.append("3.1 = Yes → Nearly all outcome data available → Low risk.")
        return Domain3Result(
            "Low",
            "Outcome data were available for nearly all participants.",
            path,
        )

    # Criterion 2: Some missing data but evidence shows no bias
    if q3_2 in YES:
        path.append("3.2 = Yes → Evidence missing data did NOT bias the result → Low risk.")
        return Domain3Result(
            "Low",
            "Missing data are unlikely to bias results based on reported evidence.",
            path,
        )

    # Criterion 3: Missingness could depend on outcome, but proportion too small to matter
    if q3_3 in YES and q3_4 in YES:
        path.append("3.3 = Yes + 3.4 = Yes → Missingness outcome-dependent but proportion small → Low risk.")
        return Domain3Result(
            "Low",
            "Missingness could depend on outcome, but the amount is too small to affect conclusions.",
            path,
        )

    # ------------------------------------------------------
    # SOME CONCERNS
    # ------------------------------------------------------
    path.append("Insufficient information to confirm low risk, but no high-risk criteria met → Some concerns.")

    return Domain3Result(
        "Some concerns",
        "There is some uncertainty regarding the potential influence of missing outcome data.",
        path,
    )
