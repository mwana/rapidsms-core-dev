#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from datetime import datetime
from django.utils.translation.trans_real import translation
from .base import MessageBase
from ..conf import settings


class OutgoingMessage(MessageBase):
    """
    """

    def __init__(self, connection=None, template=None, **kwargs):
        self._parts = []
        
        if template is not None:
            self.append(template, **kwargs)

        self._connection = connection
        self.sent_at = None

        # default to LANGUAGE_CODE from the project's settings, or fall
        # back to 'en-us', from django.conf.global_settings:39
        self.language = settings.LANGUAGE_CODE


    def append(self, template, **kwargs):
        self._parts.append((template, kwargs))


    def __repr__(self):
        return "<OutgoingMessage (%s): %s>" %\
            (self.language, self.text)


    def _render_part(self, template, **kwargs):
        t = translation(self.language)
        tmpl = t.gettext(template)
        return tmpl % kwargs


    @property
    def text(self):
        return " ".join([
            self._render_part(template, **kwargs)
            for template, kwargs in self._parts
        ])


    @property
    def date(self):
        return self.sent_at


    def send(self):
        """
        Send this message via the router, triggering the _outgoing_
        phase (giving any app the opportunity to modify or cancel it).
        Return True if the message was sent successfully.

        Warning: This method blocks the current thread until the backend
        accepts or rejects the message, which takes as long as it takes.
        There is currently no way to send messages asynchronously.
        """

        from rapidsms.router import router
        return router.outgoing(self)


    def send_now(self):
        """
        Send this message immediately via the physical backend. This
        should probably only be called by the Router.
        """

        from ..router import router
        backend_name = self.connection.backend.name
        self.sent = router.backends[backend_name].send(self)
        if self.sent: self.sent_at = datetime.now()
        return self.sent
