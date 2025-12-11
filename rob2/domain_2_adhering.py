# ============================================
# RoB 2.0 – Domain 2: Effect of Adhering to Intervention
# ============================================

from .common import (
    BaseDomain,
    DomainResult,
    NO,
    NO_INFO,
    NOT_APPLICABLE,
    Response,
    YES,
)


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
class Domain2Adhering(BaseDomain):
    """Domain implementation using the shared BaseDomain interface."""

    key = "domain_2_adhering"
    title = "Domain 2: Risk of Bias – Effect of Adhering to Intervention"
    questions = {
        "2.1": "Were participants aware of their assigned intervention during the trial?",
        "2.2": "Were carers/people delivering the interventions aware of participants’ assigned intervention?",
        "2.3": "(If Y/PY/NI to 2.1 or 2.2) Were important non-protocol interventions balanced across intervention groups?",
        "2.4": "(If applicable) Were there failures in implementing the intervention that could have affected the outcome?",
        "2.5": "(If applicable) Was there non-adherence to the assigned intervention regimen that could have affected participants’ outcomes?",
        "2.6": "(If N/PN/NI to 2.3, or Y/PY/NI to 2.4 or 2.5) Was an appropriate analysis used to estimate the effect of adhering to intervention?",
    }

    # --------------------------------------------
    # Returns next question code for adherence domain
    # --------------------------------------------
    def get_next_question(self, state: dict):
        """
        Given a state dict like:
            {"2.1": Response or None, ..., "2.6": Response or None}

        Returns:
            "2.x"  → next signalling question to answer
            None   → all questions answered
        """

        # Q2.1 – Participant awareness
        if state.get("2.1") is None:
            return "2.1"

        # Q2.2 – Carer/deliverer awareness
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
            (aware and state.get("2.3") in (NO | NO_INFO)) or
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
    def evaluate(self, q2_1, q2_2, q2_3, q2_4, q2_5, q2_6):
        """
        Executes the full RoB 2 decision tree for Domain 2 (effect of adhering).
        """

        # Validate inputs
        for q in (q2_1, q2_2, q2_3, q2_4, q2_5, q2_6):
            if q is not None and not isinstance(q, Response):
                raise ValueError(f"Invalid input: {q}. Must be a Response enum or None.")

        path = []

        aware = (q2_1 in (YES | NO_INFO)) or (q2_2 in (YES | NO_INFO))
        non_protocol_unbalanced = aware and q2_3 in NO
        non_protocol_unclear = aware and ((q2_3 in NO_INFO) or (q2_3 is None))
        implementation_failures = q2_4 in YES
        implementation_unclear = q2_4 in NO_INFO
        non_adherence_present = q2_5 in YES
        non_adherence_unclear = q2_5 in NO_INFO

        analysis_needed = (
            non_protocol_unbalanced
            or non_protocol_unclear
            or implementation_failures
            or implementation_unclear
            or non_adherence_present
            or non_adherence_unclear
        )

        reasons = []
        if non_protocol_unbalanced:
            reasons.append("Important non-protocol interventions were not balanced.")
        if non_protocol_unclear:
            reasons.append("Balance of important non-protocol interventions is unclear.")
        if implementation_failures:
            reasons.append("Failures in implementing the intervention could have affected outcomes.")
        if implementation_unclear:
            reasons.append("Information on intervention implementation is insufficient.")
        if non_adherence_present:
            reasons.append("Non-adherence to the intervention regimen could affect outcomes.")
        if non_adherence_unclear:
            reasons.append("Adherence information is insufficient to rule out bias.")

        # ------------------------------------------------------
        # HIGH RISK RULES
        # ------------------------------------------------------
        if analysis_needed and q2_6 in NO:
            path.append("Potential biases identified ({}) without an appropriate analysis → High risk.".format(
                "; ".join(reasons) if reasons else "analysis requested"
            ))
            return Domain2AdherenceResult(
                "High",
                "The adherence-effect estimate is likely biased because necessary analytical adjustments were not used.",
                path,
            )

        # ------------------------------------------------------
        # LOW RISK RULES
        # ------------------------------------------------------
        non_protocol_balanced_or_not_applicable = (not aware) or (q2_3 in YES) or (q2_3 in NOT_APPLICABLE)
        implementation_ok = q2_4 in (NO | NOT_APPLICABLE) or q2_4 is None
        adherence_ok = q2_5 in (NO | NOT_APPLICABLE) or q2_5 is None
        analysis_ok = (not analysis_needed) or (q2_6 in YES)

        if non_protocol_balanced_or_not_applicable and implementation_ok and adherence_ok and analysis_ok:
            path.append("No concerning imbalances or adherence issues and analysis appropriate when needed → Low risk.")
            return Domain2AdherenceResult(
                "Low",
                "Bias due to deviations from intended intervention is unlikely under the adherence effect.",
                path,
            )

        # ------------------------------------------------------
        # SOME CONCERNS
        # ------------------------------------------------------
        path.append(
            "Potential deviations or unclear information remain, or the appropriateness of analysis is uncertain → Some concerns."
        )
        return Domain2AdherenceResult(
            "Some concerns",
            "Some uncertainty remains about non-protocol interventions, implementation fidelity, adherence, or the analytical approach.",
            path,
        )


_DOMAIN2_ADHERING = Domain2Adhering()


# Compatibility helpers
def get_next_question_domain2_adhering(state: dict):
    return _DOMAIN2_ADHERING.get_next_question(state)


def rob2_domain2_adhering(q2_1, q2_2, q2_3, q2_4, q2_5, q2_6):
    return _DOMAIN2_ADHERING.evaluate(q2_1, q2_2, q2_3, q2_4, q2_5, q2_6)


QUESTIONS = Domain2Adhering.questions
