from uuid import UUID


from loans_billing_legacy.models.loan import Loan
from loans_billing_legacy.services.firestore.firestore import get_firestore
from loans_billing_legacy.services.firestore.lock import lock_document, release_lock


def with_locked_loan(loan_id: UUID):
    def locked_loan_decorator(func):
        async def locked_loan_wrapper(*args, **kwargs):
            firestore = get_firestore()

            loan_ref = firestore.collection("loans").document(str(loan_id))

            loan = await lock_document(loan_ref)

            if loan.exists:
                try:
                    loan = Loan(**loan.to_dict())
                except:
                    loan = None
            else:
                loan = None

            result = await func(*args, **kwargs, loan=loan, loan_ref=loan_ref)

            await release_lock(loan_ref)

            return result

        return locked_loan_wrapper

    return locked_loan_decorator
