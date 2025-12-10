# ============================================
# RoB 2.0 – Domain 4: Measurement of the Outcome
# ============================================

from .common import BaseDomain, DomainResult, NO, NO_INFO, Response, YES


class Domain4Result(DomainResult):
    def __init__(self, judgement, explanation, path):
        super().__init__(
            "Domain 4: Risk of Bias – Measurement of the Outcome",
            judgement,
            explanation,
            path,
        )


class Domain4Measurement(BaseDomain):
    """Domain implementation using the shared BaseDomain interface."""

    key = "domain_4_measurement"
    title = "Domain 4: Risk of Bias – Measurement of the Outcome"
    questions = {
        "4.1": "Was the method of measuring the outcome inappropriate?",
        "4.2": "Was the measurement or ascertainment of the outcome different between intervention groups?",
        "4.3": "Were outcome assessors aware of the intervention received by study participants?",
        "4.4": "Could assessment of the outcome have been influenced by knowledge of the intervention received?",
        "4.5": "Is it likely that assessment of the outcome was influenced by knowledge of the intervention received?",
    }

    # --------------------------------------------
    # Return next signalling question code for Domain 4
    # --------------------------------------------
    def get_next_question(self, state: dict):
        """
        Domain 4 question sequence:
            4.1 → 4.2 → 4.3 (if 4.1 and 4.2 are N/PN/NI) → 4.4 (if 4.3 = Y/PY/NI) → 4.5 (if 4.4 = Y/PY/NI)

        Returns:
            "4.x" → next question
            None  → complete
        """

        if state.get("4.1") is None:
            return "4.1"

        if state.get("4.2") is None:
            return "4.2"

        if state.get("4.3") is None and state["4.1"] in (NO | NO_INFO) and state["4.2"] in (NO | NO_INFO):
            return "4.3"

        aware_or_uncertain = state.get("4.3") in (YES | NO_INFO)

        if aware_or_uncertain and state.get("4.4") is None:
            return "4.4"

        if state.get("4.4") in (YES | NO_INFO) and state.get("4.5") is None:
            return "4.5"

        return None

    # --------------------------------------------
    # Final Risk of Bias Algorithm for Domain 4
    # --------------------------------------------
    def evaluate(self, q4_1, q4_2, q4_3, q4_4, q4_5):
        """
        Executes the full RoB 2 decision tree for Domain 4 (Outcome Measurement).
        """

        # Validate inputs
        for q in (q4_1, q4_2, q4_3, q4_4, q4_5):
            if q is not None and not isinstance(q, Response):
                raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

        path = []
        aware_or_uncertain = q4_3 in (YES | NO_INFO)
        could_be_influenced = q4_4 in (YES | NO_INFO)
        influence_likely_or_uncertain = q4_5 in (YES | NO_INFO)

        # ------------------------------------------------------
        # HIGH RISK RULES
        # ------------------------------------------------------

        # Measurement method inappropriate
        if q4_1 in YES:
            path.append("4.1 = Yes/Probably Yes → Measurement method inappropriate → High risk.")
            return Domain4Result(
                "High",
                "The method used to measure the outcome is inappropriate for the construct of interest.",
                path,
            )

        # Outcome measured differently between groups
        if q4_2 in YES:
            path.append("4.2 = Yes/Probably Yes → Outcome measurement differed between groups → High risk.")
            return Domain4Result(
                "High",
                "Outcome measurement methods differed between groups, introducing bias.",
                path,
            )

        # Awareness with possible influence and no reassurance it was avoided
        if q4_2 in (NO | NO_INFO) and aware_or_uncertain and could_be_influenced and influence_likely_or_uncertain:
            path.append("Awareness of assignment + assessment could be influenced and likely/uncertain influence → High risk.")
            return Domain4Result(
                "High",
                "Outcome assessment was likely influenced by knowledge of intervention assignment.",
                path,
            )

        # ------------------------------------------------------
        # LOW RISK RULES
        # ------------------------------------------------------

        if (
            q4_1 in (NO | NO_INFO) and
            q4_2 in NO and
            q4_3 in NO
        ):
            path.append("Measurement not inappropriate + similar across groups + assessors unaware → Low risk.")
            return Domain4Result(
                "Low",
                "Outcome measurement appears appropriate, consistent, and masked.",
                path,
            )

        if (
            q4_1 in (NO | NO_INFO) and
            q4_2 in NO and
            aware_or_uncertain and
            q4_4 in NO
        ):
            path.append("Measurement not inappropriate + similar across groups + awareness present but could not influence assessment → Low risk.")
            return Domain4Result(
                "Low",
                "Outcome measurement appears appropriate, consistent, and unlikely to be biased by awareness.",
                path,
            )

        # ------------------------------------------------------
        # SOME CONCERNS
        # ------------------------------------------------------
        if q4_1 in (NO | NO_INFO) and q4_2 in NO_INFO and q4_3 in NO:
            path.append("Measurement method not inappropriate + measurement differences unclear but assessors unaware → Some concerns.")
            return Domain4Result(
                "Some concerns",
                "Unclear whether measurement differed between groups, though assessors were blinded.",
                path,
            )

        if q4_1 in (NO | NO_INFO) and q4_2 in NO_INFO and aware_or_uncertain and q4_4 in NO:
            path.append("Measurement differences unclear + assessors aware/uncertain but influence judged not possible → Some concerns.")
            return Domain4Result(
                "Some concerns",
                "Unclear if measurement differed between groups, but assessment unlikely influenced by awareness.",
                path,
            )

        if q4_2 in (NO | NO_INFO) and aware_or_uncertain and could_be_influenced and q4_5 in NO:
            path.append("Assessors aware/uncertain + assessment could be influenced but unlikely to have been → Some concerns.")
            return Domain4Result(
                "Some concerns",
                "Awareness existed yet influence on assessment is judged unlikely.",
                path,
            )

        path.append("Insufficient evidence for low risk, but high-risk conditions not met → Some concerns.")

        return Domain4Result(
            "Some concerns",
            "There is some uncertainty regarding potential influence on outcome measurement.",
            path,
        )


_DOMAIN4 = Domain4Measurement()


# Compatibility helpers
def get_next_question_domain4(state: dict):
    return _DOMAIN4.get_next_question(state)


def rob2_domain4(q4_1, q4_2, q4_3, q4_4, q4_5):
    return _DOMAIN4.evaluate(q4_1, q4_2, q4_3, q4_4, q4_5)


QUESTIONS = Domain4Measurement.questions
