import json

import cherrypy

from dto import EventDto


class PingController(object):

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def health(self):
        print("\n health")
        return {'status': 'UP'}


class WhatsAppController(object):

    @cherrypy.tools.accept(media="application/x-www-form-urlencoded")
    @cherrypy.tools.json_out()
    def post(self, *args, **post):
        data = post.get('data', None)
        if not data:
            raise Exception('No Data object')
        print(f"\n json is {data}")
        data = json.loads(data, encoding='utf-8')
        event_dt = EventDto(data)
        print(f"\n the notification received is {event_dt}")
        if event_dt.event_name.upper() == 'INBOX':
            print("\n Should send auto reply")
            return {'autoreply': 'Hi, I got your message. Will get back to you soon.'}
        return event_dt.__dict__
