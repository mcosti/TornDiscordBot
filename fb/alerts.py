class AlertException(Exception):
    pass


class AlertTypes:
    NEW_EVENT = 'NEW_EVENT'
    NEW_MESSAGE = 'NEW_MESSAGE'
    TRAVEL_ARRIVED = 'TRAVEL_ARRIVED'
    DRUG_COOLDOWN_ZERO = 'DRUG_COOLDOWN_ZERO'
    MEDICAL_COOLDOWN_ZERO = 'MEDICAL_COOLDOWN_ZERO'
    BOOSTER_COOLDOWN_ZERO = 'BOOSTER_COOLDOWN_ZERO'
    ENERGY_FULL = 'ENERGY_FULL'
    LIFE_FULL = 'LIFE_FULL'
    NERVE_FULL = 'NERVE_FULL'
    OUT_OF_HOSPITAL = 'OUT_OF_HOSPITAL'
    OUT_OF_JAIL = 'OUT_OF_HOSPITAL'
    INVALID_KEY = 'INVALID_KEY'


class Alert:
    def __init__(self, content, type):
        try:
            getattr(AlertTypes, type)
        except AttributeError:
            raise AlertException(f"Type {type} is not a valid alert type")

        self.type = type
        self.content = content

    def to_discord(self):
        return str(self.content)

    def __repr__(self):
        return f"<Alert {self.type}> : {self.content}"


class LocalAlertsMixin:
    def __init__(self):
        super().__init__()
        self._local_alerts = []

    def check(self, new_obj):
        raise NotImplementedError()

    def get_alerts(self, new_obj):
        self.check(new_obj)
        return self._local_alerts

    def add_alert(self, alert):
        if not isinstance(alert, Alert):
            raise AlertException("Tried to add a non-alert object")
        self._local_alerts.append(alert)
