import logging
import os
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, db

from fb.mixins import Singleton
from .models import User
from .env import DATABASE_URL

logger = logging.getLogger(__name__)


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

cred = credentials.Certificate(os.path.join(__location__, 'db_cert.json'))
firebase_admin.initialize_app(cred, {
    'databaseURL': DATABASE_URL
})
users_ref = db.reference('users')


class UserAlreadyExistsException(Exception):
    """User already exists in firebase database"""
    msg = "User already exists"


class Database(metaclass=Singleton):
    def __init__(self, cache_minutes=10):
        self._users = {}
        self.last_users_get = datetime.now()
        self.cache_minutes = cache_minutes

    def get_all_users(self, invalidate_cache=False) -> [User]:
        """Returns a dictionary with the torn_id as key and <User> as value
        """
        if (
            datetime.now() < self.last_users_get + timedelta(minutes=self.cache_minutes)
            and self._users
            and not invalidate_cache
        ):
            return self._users

        else:
            logger.info("Invalidating users cache")
            self._users = {}

            users = users_ref.get()
            if not users:
                return {}

            for id, data in users.items():
                firebase_obj = data.get('user', {})
                user = User.from_firebase_obj(id, firebase_obj)
                self._users[user.id] = user
            self.last_users_get = datetime.now()

        return self._users

    @staticmethod
    def get_user(user_id: int) -> User:
        user_data = users_ref.child(str(user_id)).child('user').get()
        if user_data:
            return User.from_firebase_obj(user_id, user_data)
        return None

    @staticmethod
    def get_user_by_discord(discord_id: int) -> User:
        # TODO: Improve by using orderByChild
        db = Database()
        users = db.get_all_users()
        for user in users.values():
            if user.credentials.discord_id == discord_id:
                return user

        return None

    @staticmethod
    def save_user(user, save_torn_data=False, save_credentials=False, save_settings=False) -> None:
        """This method is designed in this way to prevent accidentally rewriting the whole object in firebase
        but also to save up on I/O"""
        args = [save_torn_data, save_credentials, save_credentials]

        if all(args) or all(not arg for arg in args):
            #  save everything
            users_ref.child(str(user.id)).child('user').set(user.to_dict())
            logging.debug(f"Saved all data for user {user.id}")

        else:
            if save_torn_data:
                Database.save_field_for_user(user, 'torn_data')
            if save_credentials:
                Database.save_field_for_user(user, 'credentials')
            if save_settings:
                Database.save_field_for_user(user, 'settings')

    @staticmethod
    def save_new_user(user: User) -> None:
        db_user = Database.get_user(user.id)
        if db_user:
            raise UserAlreadyExistsException

        Database.save_user(user)

    def delete_user(self, user: User) -> None:
        users_ref.child(str(user.id)).delete()
        self._users.pop(user.id, '')
        logger.info(f"Deleted user {user}")

    @staticmethod
    def save_field_for_user(user: User, field: str) -> None:
        user_path = users_ref.child(str(user.id)).child('user').child(field)
        data = getattr(user, field).to_dict()
        user_path.set(data)
        logging.debug(f"Saved {field} for user {user}")

    def save_on_exit(self):
        logging.debug("Database exit --- cleanup")
        for user in self._users.values():
            Database.save_user(user, save_torn_data=True)


