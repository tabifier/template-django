from notifications.channels.base import ChannelBase


class DBChannel(ChannelBase):
    
    @staticmethod
    def notify(event_name, *args, **kwargs):
        pass
