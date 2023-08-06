from enum import Enum


class TransactionKey(str, Enum):
    PRINCIPAL_TO_DISBURSE = "principal_to_disburse"
    PRINCIPAL = "principal"
    INTEREST = "interest"
    PREPAYMENTS_TO_COVER_INTEREST = "prepayments_to_cover_interest"
    PRINCIPAL_DUE = "principal_due"
    PRINCIPAL_MPD1 = "principal_mpd1"
    PRINCIPAL_MPD2 = "principal_mpd2"
    PRINCIPAL_MPD3 = "principal_mpd3"
    PRINCIPAL_MPD4 = "principal_mpd4"
    INTEREST_MPD1 = "interest_mpd1"
    INTEREST_MPD2 = "interest_mpd2"
    INTEREST_MPD3 = "interest_mpd3"
    INTEREST_MPD4 = "interest_mpd4"
    UNHANDLED_FUNDS = "unhandled_funds"
