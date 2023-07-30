from uuid import UUID


async def get_loan_by_loan_id(loan_id: UUID):
    return {"Loan ID": loan_id}
