from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from django.utils import timezone
from django.conf import settings
import pytz
import datetime
from datetime import date

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        token = model.objects.filter(key=key).first()
        today = date.today()
        if token == None:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.datetime.now(tz=timezone.utc)
        utc_date_now = datetime.datetime.now(tz=timezone.utc)

        # expired token after 24 hour or 30 day
        if token.created.astimezone(tz=timezone.utc) < utc_now - settings.TOKEN_EXPIRE_TIME:
            token.delete()
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
