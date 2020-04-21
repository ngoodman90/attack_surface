from peewee import SqliteDatabase, Model, CharField, ManyToManyField, ForeignKeyField, DateTimeField, BigIntegerField

DATABASE = 'tweepee.db'

db = SqliteDatabase(DATABASE, pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db


class Tag(BaseModel):
    tag = CharField(unique=True, index=True)


class VirtualMachine(BaseModel):
    vm_id = CharField(unique=True, index=True)
    name = CharField()
    tags = ManyToManyField(Tag, backref='vms', on_delete='CASCADE')


VirtualMachineTag = VirtualMachine.tags.get_through_model()


class FirewallRule(BaseModel):
    fw_id = CharField(unique=True, index=True)
    source_tag = ForeignKeyField(Tag, backref='fw_sources', on_delete='CASCADE')
    dest_tag = ForeignKeyField(Tag, backref='fw_dests', on_delete='CASCADE')


class RequestStat(BaseModel):
    start_time = DateTimeField(index=True)
    end_time = DateTimeField()
    diff = BigIntegerField(index=True, help_text='diff in microseconds')


class ServerProcess(BaseModel):
    start_time = DateTimeField(index=True)


def tables_exist() -> bool:
    return bool(db.get_tables())


MODELS = [
    Tag,
    VirtualMachine,
    VirtualMachineTag,
    FirewallRule,
    RequestStat,
    ServerProcess
]


def create_tables():
    with db:
        db.create_tables(MODELS)
