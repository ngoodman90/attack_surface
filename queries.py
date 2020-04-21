from typing import List, Dict
from peewee import fn

from models import VirtualMachine, ServerProcess, RequestStat

MICROSECONDS_TO_MILLI = 1000


def potential_attackers(vm_id: str) -> List[str]:
    try:
        vm_obj = VirtualMachine.get(vm_id=vm_id)
    except VirtualMachine.DoesNotExist:
        raise ValueError("VM with matching id does not exists")

    source_tags = []
    for t in vm_obj.tags:
        source_tags += [f.source_tag for f in t.fw_dests]

    potential_attacker_ids = []
    for t in source_tags:
        potential_attacker_ids += [v.vm_id for v in t.vms]
    if vm_id in potential_attacker_ids:
        potential_attacker_ids.remove(vm_id)

    return potential_attacker_ids


def get_stats() -> Dict:
    last_process_start_time = ServerProcess.select().order_by(ServerProcess.start_time.desc()).get().start_time
    vm_count = VirtualMachine.select().count()
    request_count = RequestStat.select().where(RequestStat.start_time > last_process_start_time).count()

    avg_milli = 0
    if request_count > 0:
        total_time = \
            RequestStat.select(
                fn.SUM(RequestStat.diff)
            ).where(
                RequestStat.start_time > last_process_start_time
            ).scalar()
        avg_milli = total_time / request_count / MICROSECONDS_TO_MILLI

    return {
        "vm_count": vm_count,
        "request_count": request_count,
        "average_request_time": avg_milli
    }
