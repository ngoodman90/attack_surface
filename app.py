import falcon

from resources import VmAttackers, Stats

api = application = falcon.API()

api.add_route('/api/v1/attack', VmAttackers())
api.add_route('/api/v1/stats', Stats())
