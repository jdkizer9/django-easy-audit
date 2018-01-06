from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.signals import request_started
from django.http.cookie import SimpleCookie
from django.utils import six, timezone
from django.conf import settings

from easyaudit.models import RequestEvent
<<<<<<< HEAD
from easyaudit.settings import UNREGISTERED_URLS, WATCH_REQUEST_EVENTS
from easyaudit.utils import get_client_ip
=======
from easyaudit.settings import REMOTE_ADDR_HEADER, UNREGISTERED_URLS, WATCH_REQUEST_EVENTS
>>>>>>> master

import re


def should_log_url(url):
    # check if current url is blacklisted
    for unregistered_url in UNREGISTERED_URLS:
        pattern = re.compile(unregistered_url)
        if pattern.match(url):
            return False
    return True

def request_started_handler(sender, environ, **kwargs):
    if not should_log_url(environ['PATH_INFO']):
        return

    # get the user from cookies
    user = None
    if environ.get('HTTP_COOKIE'):
        cookie = SimpleCookie() # python3 compatibility
        cookie.load(environ['HTTP_COOKIE'])

        session_cookie_name = settings.SESSION_COOKIE_NAME
        if session_cookie_name in cookie:
            session_id = cookie[session_cookie_name].value

            try:
                session = Session.objects.get(session_key=session_id)
            except Session.DoesNotExist:
                session = None

            if session:
                user_id = session.get_decoded().get('_auth_user_id')
                try:
                    user = get_user_model().objects.get(id=user_id)
                except:
                    user = None

    request_event = RequestEvent.objects.create(
        url=environ['PATH_INFO'],
        method=environ['REQUEST_METHOD'],
        query_string=environ['QUERY_STRING'],
        user=user,
<<<<<<< HEAD
        remote_ip=get_client_ip(environ),
=======
        remote_ip=environ[REMOTE_ADDR_HEADER],
>>>>>>> master
        datetime=timezone.now()
    )


if WATCH_REQUEST_EVENTS:
    request_started.connect(request_started_handler, dispatch_uid='easy_audit_signals_request_started')
