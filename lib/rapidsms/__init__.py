#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


from .apps.base import AppBase as App
from .messages import OutgoingMessage as Message


def get_rapidsms_version ():
    try:
        # do we have a static version set from an install?
        from __version__ import VERSION as version
    except ImportError:
        # if not, can we figure it out from the git tag?
        import commands
        try:
            # see http://stackoverflow.com/questions/62264/#72874
            version = commands.getoutput("git describe --tags")
        except:
            # otherwise, give up!
            version = "unknown"
    return version
