from originations.enums.policy import PolicyOutcome
from fastapi import status
from fastapi.responses import JSONResponse


def application_result(
    outcome: PolicyOutcome, acceptable_quotes: list = []
) -> JSONResponse:
    """
    Returns the result of an application.

    Note that this function should NOT be used for submissions - a seperate endpoint is necessary.

    """

    if outcome in [
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
    ]:
        body = {"Outcome": "Application Declined", "Acceptable Quotes": []}
    elif outcome in [
        PolicyOutcome.REFERRED,
        PolicyOutcome.REFERRED_DUE_TO_TECHNICAL_ERROR,
    ]:
        body = {"Outcome": "Application Declined", "Acceptable Quotes": []}
    elif outcome == PolicyOutcome.PASSED:
        # TODO - raise error for an approved application with no acceptable quotes
        body = {
            "Outcome": "Application Approved",
            "Acceptable Quotes": acceptable_quotes,
        }

    return JSONResponse(body, status_code=status.HTTP_200_OK)
