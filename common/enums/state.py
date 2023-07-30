from enum import Enum


class LoanState(str, Enum):
    PENDING = "pending"
    LIVE = "live"
    MPD1 = "mpd1"
    MPD2 = "mpd2"
    MPD3 = "mpd3"
    MPD4 = "mpd4"
    DEFAULTED = "defaulted"
    CLOSED = "closed"
    CLOSED_INITIATED = "closed_initiated"
