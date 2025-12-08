# ============================================
# RoB 2.0 – Domain 2: Effect of Assignment to Intervention
# ============================================

from .common import DomainResult, NO, NO_INFO, Response, YES


class Domain2Result(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 2: Risk of Bias – Effect of Assignment to Intervention",
            judgement,
            explanation,
            path,
        )


def get_next_question_domain2(state: dict):
    """
    Given a state dict like:
        {"2.1": Response or None, ..., "2.7": Response or None}

    Returns:
        "2.x"  → next signalling question to answer
        None   → all questions answered
    """

    # Q2.1
    if state.get("2.1") is None:
        return "2.1"

    # Q2.2
    if state.get("2.2") is None:
        return "2.2"

    aware = (state["2.1"] in (YES | NO_INFO)) or (state["2.2"] in (YES | NO_INFO))

    # Q2.3 – only if awareness exists
    if aware:
        if state.get("2.3") is None:
            return "2.3"

        # Q2.4 – only if deviations occurred
        if state["2.3"] in YES:
            if state.get("2.4") is None:
                return "2.4"

            # Q2.5
            if state.get("2.5") is None and state["2.4"] in (YES | NO_INFO):
                return "2.5"

    # Q2.6 – always needed
    if state.get("2.6") is None:
        return "2.6"

    # Q2.7 – only if analysis inappropriate
    if state["2.6"] in (NO | NO_INFO) and state.get("2.7") is None:
        return "2.7"

    # Complete
    return None


# --------------------------------------------
# Final Risk of Bias Algorithm for Domain 2
# --------------------------------------------
def rob2_domain2(q2_1, q2_2, q2_3, q2_4, q2_5, q2_6, q2_7):
    """
    Executes the full RoB 2 decision tree for Domain 2.
    """

    # Validate inputs
    for q in (q2_1, q2_2, q2_3, q2_4, q2_5, q2_6, q2_7):
        if q is not None and not isinstance(q, Response):
            raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

    path = []

    aware = (q2_1 in YES) or (q2_2 in YES)

    # ------------------------------------------------------
    # HIGH RISK RULES
    # ------------------------------------------------------

    # Awareness + deviations + effect on outcome
    if aware and q2_3 in YES and q2_4 in YES:
        path.append("Participants/carers aware → deviations due to trial → deviations affect outcome → High risk.")
        return Domain2Result("High",
                             "Knowledge of assignment led to deviations likely to influence outcomes.",
                             path)

    # Awareness + deviations not balanced
    if aware and q2_3 in YES and q2_5 in NO:
        path.append("Deviations due to trial were not balanced between groups → High risk.")
        return Domain2Result("High",
                             "Deviations occurred in a way that likely introduced bias.",
                             path)

    # Analysis inappropriate + likely biased
    if q2_6 in NO and q2_7 in YES:
        path.append("Inappropriate analysis + likely biased → High risk.")
        return Domain2Result("High",
                             "The effect estimate is likely biased due to inappropriate analysis.",
                             path)

    # ------------------------------------------------------
    # LOW RISK RULES
    # ------------------------------------------------------

    # No awareness OR awareness but no problematic deviations + appropriate analysis
    if (not aware or q2_3 in (NO | NO_INFO)) and (q2_6 in YES | NO_INFO):
        path.append("No awareness or no concerning deviations + appropriate ITT analysis → Low risk.")
        return Domain2Result("Low",
                             "Assignment awareness did not bias outcomes and analysis method was appropriate.",
                             path)

    # ------------------------------------------------------
    # SOME CONCERNS
    # ------------------------------------------------------
    path.append("Conditions for high risk not met; conditions for low risk not fully satisfied → Some concerns.")
    return Domain2Result("Some concerns",
                         "Some uncertainty remains about deviations or the appropriateness of the analysis.",
                         path)
