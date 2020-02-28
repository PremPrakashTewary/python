import cherrypy

from controller.whatsapp_webhook import PingController, WhatsAppController

if __name__ == '__main__':
    ping_controller = PingController()
    whatsapp_controller = WhatsAppController()
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.explicit = False
    dispatcher.connect(name='health_check', route='/v1/:action/', controller=ping_controller, action='health',
                       conditions=dict(method=['GET']))
    dispatcher.connect(name='test_post', route='/v1/:action/', controller=whatsapp_controller, action='post',
                       conditions=dict(method=['POST']))
    conf = {'/': {'request.dispatch': dispatcher, 'tools.json_in.force': False}}
    cherrypy.config.update({'global': {
        'environment': 'production',
        'log.screen': False,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8088,
        'tools.caching.on': False,
        'tools.encode.encoding': "utf-8",
        'tools.json_in.on': True,
        'tools.json_in.force': False,
        'request.dispatch': dispatcher
    }})
    cherrypy.quickstart(root=None, config=conf)
