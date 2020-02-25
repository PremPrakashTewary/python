class EventDto:

    def __init__(self, event_name, from_no, to_no, text_msg):
        self.event_name = event_name
        self.from_no = from_no
        self.to_no = to_no
        self.text_msg = text_msg

    def __str__(self):
        return str(self.__dict__)