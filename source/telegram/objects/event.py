class Event:
    def __init__(self, telegram_id, type, **kwargs):
        self.telegram_id = telegram_id
        self.type = type
        self.objects = kwargs