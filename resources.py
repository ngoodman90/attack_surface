import json
import falcon

from queries import potential_attackers, get_stats
from utils import timed_request


class VmAttackers:
    @timed_request
    def on_get(self, req, resp):
        print(req.params)
        try:
            pot_attackers = potential_attackers(req.params['vm_id'])
            resp.body = json.dumps({"vm_ids": pot_attackers})
        except ValueError as e:
            resp.body = json.dumps({"error": str(e)})
            resp.status = falcon.HTTP_400


class Stats:
    @timed_request
    def on_get(self, req, resp):
        resp.body = json.dumps(get_stats())
