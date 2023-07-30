# type: ignore

from pydantic import BaseSettings


class LoansBillingSettings(BaseSettings):
    project_id: str
    client_id: str
    client_x509_cert_url: str
    firebase_private_key_id: str
    firebase_client_email: str
    environment: str

    # repayment_received_subscription_id: str
    loan_creation_requested_subscription_id: str
    # loan_force_closed_subscription_id: str
    # loan_behaviour_override_applied_subscription_id: str
    loan_event_topic_id: str
    loan_event_reporting_topic_id: str

    class Config:
        env_file = ".env"


settings = LoansBillingSettings()
