import collections
import logging
import os
import textwrap
from smalld import SmallD, Intent

from .message_modification import MessageModification

LOG_CHANNEL_ID = os.environ.get("AIO_CHANNEL_ID")


logging.basicConfig(level=logging.INFO)


smalld = SmallD(token=os.environ.get("AIO_TOKEN"), intents=Intent.GUILD_MESSAGES)

def log(what):
    smalld.post(
        f"/channels/{LOG_CHANNEL_ID}/messages",
        { "content" : textwrap.dedent(what) + "\n_ _"})

def register(cls, *args, **kwargs):
    instance = cls(*args, **kwargs, log=log)

    def dispatch(payload):
        if (payload.op != 0):
            return

        method = f"on_{payload.t.lower()}"

        try:
            getattr(instance, method)(payload.d)
        except AttributeError:
            pass

    smalld.on_gateway_payload(op=0)(dispatch)



register(MessageModification) 

smalld.run()

