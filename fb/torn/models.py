from fb.alerts import Alert, AlertTypes, LocalAlertsMixin
from fb.mixins import ToDictMixin
from fb.utils import strip_html
from fb.date_utils import torn_now_timestamp


class Notifications(ToDictMixin):
    def __init__(self, messages=0, events=0, awards=0, competition=0, **kwargs):
        self.competition = competition
        self.awards = awards
        self.events = events
        self.messages = messages


class Event(ToDictMixin):
    def __init__(self, event='', seen=True, **kwargs):
        self.event = event
        self.seen = seen

    def alert_new(self):
        return Alert(f"New event: {strip_html(self.event)}", AlertTypes.NEW_EVENT)


class Message(ToDictMixin):
    def __init__(self, name='', title='', seen=True, **kwargs):
        self.name = name
        self.title = title
        self.seen = seen

    def alert_new(self):
        return Alert(f"New message from {self.name}: {self.title}", AlertTypes.NEW_MESSAGE)


class Travel(ToDictMixin, LocalAlertsMixin):
    def __init__(self, destination='Torn', time_left=0, **kwargs):
        super().__init__()
        self.destination = destination
        self.time_left = time_left

    def check(self, new_travel):
        if self.time_left != 0 and new_travel.time_left == 0:
            self.add_alert(Alert(f"You have arrived to {new_travel.destination}", AlertTypes.TRAVEL_ARRIVED))


class BarMixin(ToDictMixin, LocalAlertsMixin):
    name = ''
    FULL_TYPE = ''

    def __init__(self, current=-1, maximum=-1, **kwargs):
        super().__init__()
        self.current = current
        self.maximum = maximum

    @property
    def is_max(self):
        return (self.current + self.maximum > 0) and self.current == self.maximum

    def check(self, new_obj):
        if not self.is_max and new_obj.is_max:
            self.add_alert(Alert(f"Your {self.name} is full", self.FULL_TYPE))


class Energy(BarMixin):
    name = 'Energy'
    FULL_TYPE = AlertTypes.ENERGY_FULL


class Nerve(BarMixin):
    name = 'Nerve'
    FULL_TYPE = AlertTypes.NERVE_FULL


class Life(BarMixin):
    name = 'Life'
    FULL_TYPE = AlertTypes.LIFE_FULL


class Cooldowns(ToDictMixin, LocalAlertsMixin):
    def __init__(self, drug=0, medical=0, booster=0, **kwargs):
        super().__init__()
        self.drug = drug
        self.medical = medical
        self.booster = booster

    def check(self, new_cooldowns):
        if self.drug != 0 and new_cooldowns.drug == 0:
            self.add_alert(Alert("Your drugs cooldown ended", AlertTypes.DRUG_COOLDOWN_ZERO))

        if self.medical != 0 and new_cooldowns.medical == 0:
            self.add_alert(Alert("Your medical cooldown ended", AlertTypes.MEDICAL_COOLDOWN_ZERO))

        if self.booster != 0 and new_cooldowns.booster == 0:
            self.add_alert(Alert("Your boosters cooldown ended", AlertTypes.BOOSTER_COOLDOWN_ZERO))


class Status(ToDictMixin, LocalAlertsMixin):
    def __init__(self, state='okay', until=0, **kwargs):
        super().__init__()
        self.state = state.lower()
        self.until = until

    @property
    def is_in_hospital(self):
        return 'hospital' in self.state

    @property
    def is_okay(self):
        return 'okay' in self.state

    @property
    def is_in_jail(self):
        return 'jail' in self.state

    def check(self, new_status):
        if self.is_in_hospital and new_status.is_okay:
            self.add_alert(Alert("You got out of the hospital", AlertTypes.OUT_OF_HOSPITAL))

        if self.is_in_jail and new_status.is_okay:
            self.add_alert(Alert("You got out of jail", AlertTypes.OUT_OF_HOSPITAL))


class TornData:
    def __init__(
            self,
            player_id=-1,
            name='',
            server_time=torn_now_timestamp(),
            notifications: Notifications = Notifications(),
            events: [Event] = None,
            messages: [Message] = None,
            travel: Travel = Travel(),
            cooldowns: Cooldowns = Cooldowns(),
            life: Life = Life(),
            nerve: Nerve = Nerve(),
            energy: Energy = Energy(),
            status: Status = Status(),
            **kwargs
    ):
        self.player_id = player_id
        self.name = name
        self.server_time = server_time
        self.notifications = notifications
        self.events = events
        self.messages = messages
        self.travel = travel
        self.cooldowns = cooldowns
        self.life = life
        self.nerve = nerve
        self.energy = energy
        self.status = status

    def to_dict(self):
        return {
            'server_time': self.server_time,
            'player_id': self.player_id,
            'name': self.name,
            'travel': self.travel.to_dict(),
            'cooldowns': self.cooldowns.to_dict(),
            'life': self.life.to_dict(),
            'nerve': self.nerve.to_dict(),
            'energy': self.energy.to_dict(),
            'status': self.status.to_dict()
        }

    def __repr__(self):
        return str(self.__dict__)

    @classmethod
    def from_data(cls, data):
        server_time = data.get('server_time', torn_now_timestamp())
        player_id = data.get('player_id')
        name = data.get('name')
        notifications = Notifications(**data.get('notifications', {}))
        events = [Event(**event) for event in dict(data.get('events', {})).values()]
        messages = [Message(**message) for message in dict(data.get('messages', {})).values()]
        travel = Travel(**data.get('travel', {}))
        cooldowns = Cooldowns(**data.get('cooldowns', {}))
        life = Life(**data.get('life', {}))
        nerve = Nerve(**data.get('nerve', {}))
        energy = Energy(**data.get('energy', {}))
        status = Status(**data.get('status', {}))

        return cls(
            server_time=server_time,
            player_id=player_id,
            name=name,
            notifications=notifications,
            events=events,
            messages=messages,
            travel=travel,
            cooldowns=cooldowns,
            life=life,
            nerve=nerve,
            energy=energy,
            status=status
        )

