from enum import Enum

class PlayerActions(Enum):
    NO_ACTION = 0
    CHECK = 1
    CALL = 2
    RAISE = 3
    ALL_IN = 4
    FOLD = 5