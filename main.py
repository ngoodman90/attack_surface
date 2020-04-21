import datetime
import json
import subprocess
from functools import reduce

from models import VirtualMachine, Tag, FirewallRule, create_tables, tables_exist, ServerProcess

BATCH_SIZE = 999


def populate_data(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)

    vms = data['vms']
    fw_rules = data['fw_rules']

    vm_tags = reduce(lambda tags, v: tags + v['tags'], vms, [])
    fw_tags = reduce(lambda tags, fwr: tags + [fwr['source_tag'], fwr['dest_tag']], fw_rules, [])
    tag_objs = [Tag(tag=t) for t in list(set(vm_tags + fw_tags))]
    Tag.bulk_create(tag_objs, batch_size=BATCH_SIZE)

    for vm in vms:
        vm_obj = VirtualMachine.create(vm_id=vm['vm_id'], name=vm['name'])
        vm_obj.tags.add(Tag.select().where(Tag.tag.in_(vm['tags'])))

    fw_objs = [FirewallRule(fw_id=fw['fw_id'],
                            source_tag=Tag.get(tag=fw['source_tag']),
                            dest_tag=Tag.get(tag=fw['dest_tag']))
               for fw in fw_rules]
    FirewallRule.bulk_create(fw_objs, batch_size=BATCH_SIZE)


def setup():
    if not tables_exist():
        create_tables()
        populate_data('init_data.json')


def runserver():
    ServerProcess.create(start_time=datetime.datetime.now())
    bash_command = """gunicorn app"""
    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def main():
    setup()
    runserver()


if __name__ == '__main__':
    main()
