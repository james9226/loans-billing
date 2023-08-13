from enum import Enum


class TransactionKey(str, Enum):
    PRINCIPAL_TO_DISBURSE = "principal_to_disburse"
    PRINCIPAL = "principal"
    INTEREST = "interest"
    PRINCIPAL_AMOUNT_TO_COVER_INTEREST = "principal_amount_to_cover_interest"
    PRINCIPAL_DUE = "principal_due"
    PRINCIPAL_MPD1 = "principal_mpd1"
    PRINCIPAL_MPD2 = "principal_mpd2"
    PRINCIPAL_MPD3 = "principal_mpd3"
    PRINCIPAL_MPD4_PLUS = "principal_mpd4_plus"
    INTEREST_MPD1 = "interest_mpd1"
    INTEREST_MPD2 = "interest_mpd2"
    INTEREST_MPD3 = "interest_mpd3"
    INTEREST_MPD4_PLUS = "interest_mpd4_plus"
    UNHANDLED_FUNDS = "unhandled_funds"
