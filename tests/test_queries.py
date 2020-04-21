import datetime
from unittest import TestCase

from peewee import SqliteDatabase

from models import MODELS, RequestStat, ServerProcess, VirtualMachine, Tag, FirewallRule
from queries import get_stats, potential_attackers

TEST_DATABASE = 'testweepee.db'

test_db = SqliteDatabase(TEST_DATABASE, pragmas={'foreign_keys': 1})


class QueryTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not cls.tables_exist():
            cls.create_test_tables()

    @staticmethod
    def tables_exist() -> bool:
        return bool(test_db.get_tables())

    @staticmethod
    def create_test_tables():
        with test_db:
            test_db.create_tables(MODELS)

    def test_stats_when_after_server_restart_then_request_count_zero(self):
        ServerProcess.delete().execute()
        RequestStat.delete().execute()

        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        RequestStat.create(start_time=start_time, end_time=end_time, diff=(end_time - start_time).microseconds)
        ServerProcess.create(start_time=datetime.datetime.now())

        self.assertEqual(0, get_stats()['request_count'])

    def test_stats_when_not_after_server_restart_then_request_count_one(self):
        ServerProcess.delete().execute()
        RequestStat.delete().execute()

        ServerProcess.create(start_time=datetime.datetime.now())
        start_time = datetime.datetime.now()
        end_time = datetime.datetime.now()
        RequestStat.create(start_time=start_time, end_time=end_time, diff=(end_time - start_time).microseconds)

        self.assertEqual(1, get_stats()['request_count'])

    def test_stats_when_one_vm_exists_then_one_returned(self):
        VirtualMachine.delete().execute()
        VirtualMachine.create(vm_id='1', name='test_vm')
        self.assertEqual(1, get_stats()['vm_count'])

    def test_attacked_vms_when_vm_does_not_exist_then_error_raised(self):
        with self.assertRaises(ValueError):
            potential_attackers("id that does not exist")

    def test_attacked_vms_when_attacker_vm_exists_then_id_returned(self):
        VirtualMachine.delete().execute()
        Tag.delete().execute()
        FirewallRule.delete().execute()

        t1 = Tag.create(tag='test_tag_1')
        t2 = Tag.create(tag='test_tag_2')
        vm_1 = VirtualMachine.create(vm_id='1', name='test_vm_1')
        vm_1.tags.add(t1)
        vm_2 = VirtualMachine.create(vm_id='2', name='test_vm_2')
        vm_2.tags.add(t2)
        FirewallRule.create(fw_id='test_fw_1', source_tag=t1, dest_tag=t2)

        self.assertEqual([vm_1.vm_id], potential_attackers(vm_2.vm_id))
