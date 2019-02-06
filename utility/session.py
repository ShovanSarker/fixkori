from utility import UUID

from fixkori_api.models import LoginSession
# import users.mo


class Session:

    def __init__(self):
        pass

    @staticmethod
    def session_update(user):
        previous_session = LoginSession.objects.get(user=user)
        previous_session.delete()
        token = UUID.uuid_generator()
        new_session = LoginSession(user=user,
                                   token=token)
        new_session.save()
        return token

    @staticmethod
    def session_delete(token):
        previous_session = LoginSession.objects.get(token=token)
        previous_session.delete()

    @staticmethod
    def session_create(user):
        if LoginSession.objects.filter(user=user).exists():
            return Session.session_update(user)
        else:
            token = UUID.uuid_generator()
            new_session = LoginSession(user=user,
                                       token=token)
            new_session.save()
            return token

    @staticmethod
    def get_user_by_session(token):
        if LoginSession.objects.filter(token=token).exists():
            session = LoginSession.objects.get(token=token)
            return session.user
        else:
            return None
