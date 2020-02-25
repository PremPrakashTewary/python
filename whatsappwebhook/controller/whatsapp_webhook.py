import json

import cherrypy

from dto import EventDto


class PingController(object):

    def __init__(self):
        pass

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def health(self):
        print("\n health")
        return {'status': 'UP'}

    def __call__(self, *args, **kwargs):
        pass


class WhatsAppController(object):

    def __init__(self):
        pass

    @cherrypy.tools.accept(media="application/x-www-form-urlencoded")
    @cherrypy.tools.json_out()
    def post(self, *args, **post):
        data = post.get('data', None)
        if not data:
            raise Exception('No Data object')
        print(f"\n json is {data}")
        data = json.loads(data, encoding='utf-8')
        event_dt = EventDto(data['event'], data['from'], data['to'], data['text'])
        print(f"\n the notification received is {event_dt}")
        return event_dt.__dict__

    def __call__(self, *args, **kwargs):
        pass
