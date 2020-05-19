from fb.mixins import ToDictMixin
from fb.torn.models import TornData


class Settings(ToDictMixin):
    def __init__(
            self,
            enable_global=True,
            enable_events=True,
            enable_messages=True,
            enable_travel=True,
            enable_cooldowns=True,
            enable_life=True,
            enable_nerve=True,
            enable_energy=True,
            enable_status=True,
            poll_seconds=30
    ):
        self.enable_global = enable_global
        self.enable_events = enable_events
        self.enable_messages = enable_messages
        self.enable_travel = enable_travel
        self.enable_cooldowns = enable_cooldowns
        self.enable_life = enable_life
        self.enable_nerve = enable_nerve
        self.enable_energy = enable_energy
        self.enable_status = enable_status
        # self.poll_seconds = poll_seconds


class Credentials(ToDictMixin):
    def __init__(
            self,
            torn_key='',
            torn_key_valid=True,
            discord_id='',
            active_until='',
    ):
        self.torn_key = torn_key
        self.torn_key_valid = torn_key_valid
        self.discord_id = int(discord_id) if discord_id else None
        self.active_until = active_until


class User:
    def __init__(
            self,
            id: int,
            torn_data: TornData,
            credentials: Credentials,
            settings: Settings = Settings(),
    ):
        self.id = id
        self.settings = settings
        self.torn_data = torn_data
        self.credentials = credentials

    def to_dict(self):
        return {
            'settings': self.settings.to_dict(),
            'torn_data': self.torn_data.to_dict(),
            'credentials': self.credentials.to_dict()
        }

    def __repr__(self):
        return f"<User {self.id}>"

    @property
    def params(self):
        return {
            'key': self.credentials.torn_key,
            'selections': 'notifications,events,messages,travel,cooldowns,bars,basic,icons',
            'from': self.torn_data.server_time
        }

    @classmethod
    def from_firebase_obj(cls, id, user):
        settings = Settings(**user.get('settings', {}))
        torn_data = TornData.from_data(user.get('torn_data', {}))
        credentials = Credentials(**user.get('credentials', {}))
        return cls(id=int(id), settings=settings, torn_data=torn_data, credentials=credentials)

    @classmethod
    def create_new_user(cls, torn_data, credentials):
        return cls(id=torn_data.player_id, torn_data=torn_data, credentials=credentials)

    def save(self, save_torn_data=False, save_credentials=False, save_settings=False):
        from fb.database import Database

        Database.save_user(
            user=self,
            save_torn_data=save_torn_data,
            save_credentials=save_credentials,
            save_settings=save_settings
        )

    def transfer_user(self, new_discord_id):
        self.credentials.discord_id = new_discord_id
        self.save(save_credentials=True)


class DataComparator:
    def __init__(self, old_data: TornData, new_data: TornData, settings: Settings):
        self.old_data = old_data
        self.new_data = new_data
        self.settings = settings
        self.alerts = []

    def check_events(self):
        if not self.settings.enable_events:
            return

        if self.new_data.notifications.events:
            for event in self.new_data.events:
                if not event.seen:
                    self.alerts.append(event.alert_new())

    def check_messages(self):
        if not self.settings.enable_messages:
            return

        if self.new_data.notifications.messages:
            for message in self.new_data.messages:
                if not message.seen:
                    self.alerts.append(message.alert_new())

    def check_travel(self):
        if self.settings.enable_travel:
            self.alerts.extend(self.old_data.travel.get_alerts(self.new_data.travel))

    def check_cooldowns(self):
        if self.settings.enable_cooldowns:
            self.alerts.extend(self.old_data.cooldowns.get_alerts(self.new_data.cooldowns))

    def check_bars(self):
        if self.settings.enable_energy:
            self.alerts.extend(self.old_data.energy.get_alerts(self.new_data.energy))

        if self.settings.enable_nerve:
            self.alerts.extend(self.old_data.nerve.get_alerts(self.new_data.nerve))

        if self.settings.enable_life:
            self.alerts.extend(self.old_data.life.get_alerts(self.new_data.life))

    def check_status(self):
        if self.settings.enable_status:
            self.alerts.extend(self.old_data.status.get_alerts(self.new_data.status))

    def compute_alerts(self):
        if not self.settings.enable_global:
            return []

        self.check_events()
        self.check_messages()
        self.check_travel()
        self.check_cooldowns()
        self.check_bars()
        self.check_status()

        return self.alerts

