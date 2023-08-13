import hashlib
from originations.models.request import ApplicationRequestInput


def hash_application(raw_request: ApplicationRequestInput):
    string = (
        raw_request.first_name
        + raw_request.last_name
        + raw_request.email
        + str(raw_request.date_of_birth)
    )
    return hashlib.sha256(string.encode("utf-8")).hexdigest()
