import collections

class MessageModification:
    def __init__(self, log):
        self.log = log
        self.message_log = collections.deque(maxlen=5000)

    def on_message_create(self, msg):
        self.message_log.append(msg)

    def on_message_update(self, msg):
        old = next(m for m in self.message_log if m.id == msg.id)

        self.log(
            f"""
            \u270E Message from {old.author.username}#{old.author.discriminator} edited.
            from:
            > {old.content}

            to:
            > {msg.content}
            """
        )

    def on_message_delete(self, deleted):
        old = next(m for m in self.message_log if m.id == deleted.id)

        self.log(
            f"""
            \u274C Message from {old.author.username}#{old.author.discriminator} deleted.
            > {old.content}
            """
        )

