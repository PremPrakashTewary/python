class EventDto:

    def __init__(self, event_data_dict):
        self.event_name = event_data_dict['event']
        self.from_no = event_data_dict['from']
        self.to_no = event_data_dict['to']
        self.text_msg = event_data_dict.get('text', None)
        self.custom_data = event_data_dict.get('custom_data', None)

    def __str__(self):
        class_name = str(self.__class__.__name__)
        class_name = {class_name: self.__dict__}
        return str(class_name)