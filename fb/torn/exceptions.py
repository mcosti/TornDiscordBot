class TornErrorCode:
    UNKNOWN_ERROR = 0
    KEY_EMPTY = 1
    KEY_INCORRECT = 2
    WRONG_TYPE = 3
    WRONG_FIELDS = 4
    TOO_MANY_REQUESTS = 5
    INCORRECT_ID = 6
    INCORRECT_ID_ENTITY = 7
    IP_BLOCK = 8
    API_DISABLED = 9
    FEDERAL_JAIL = 10
    KEY_CHANGE_ERROR = 11
    KEY_READ_ERROR = 12



USERS_FAULT = [
    TornErrorCode.KEY_EMPTY,
    TornErrorCode.KEY_INCORRECT,
    TornErrorCode.FEDERAL_JAIL
]


SERVERS_FAULT = [
    TornErrorCode.WRONG_TYPE,
    TornErrorCode.WRONG_FIELDS,
    TornErrorCode.TOO_MANY_REQUESTS,
    TornErrorCode.INCORRECT_ID,
    TornErrorCode.INCORRECT_ID_ENTITY,
    TornErrorCode.IP_BLOCK
]

TORNS_FAULT = [
    TornErrorCode.API_DISABLED,
    TornErrorCode.KEY_CHANGE_ERROR,
    TornErrorCode.KEY_READ_ERROR
]


class TornException(Exception):
    def __init__(self, code, error, user_id=None):
        self.code = code
        self.error = error
        self.user_id = user_id

    def __repr__(self):
        return f'Torn API Error Code {self.code}: {self.error} - User {self.user_id}'

    def __str__(self):
        return self.__repr__()

    @property
    def users_fault(self):
        return self.code in USERS_FAULT

    @property
    def servers_fault(self):
        return self.code in SERVERS_FAULT

    @property
    def torns_fault(self):
        return self.code in TORNS_FAULT
