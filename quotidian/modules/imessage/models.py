from peewee import *

database = Proxy()

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class Sqlitedatabaseproperties(BaseModel):
    key = TextField(null=True, unique=True)
    value = TextField(null=True)

    class Meta:
        db_table = '_SqliteDatabaseProperties'

class Attachment(BaseModel):
    rowid = PrimaryKeyField(db_column='ROWID', null=True)
    created_date = IntegerField(null=True)
    filename = TextField(null=True)
    guid = TextField(unique=True)
    is_outgoing = IntegerField(null=True)
    mime_type = TextField(null=True)
    start_date = IntegerField(null=True)
    total_bytes = IntegerField(null=True)
    transfer_name = TextField(null=True)
    transfer_state = IntegerField(null=True)
    user_info = BlobField(null=True)
    uti = TextField(null=True)

    class Meta:
        db_table = 'attachment'

class Chat(BaseModel):
    rowid = PrimaryKeyField(db_column='ROWID', null=True)
    account = TextField(db_column='account_id', null=True)
    account_login = TextField(null=True)
    chat_identifier = TextField(index=True, null=True)
    display_name = TextField(null=True)
    group = TextField(db_column='group_id', null=True)
    guid = TextField(unique=True)
    is_archived = IntegerField(index=True, null=True)
    is_filtered = IntegerField(null=True)
    last_addressed_handle = TextField(null=True)
    properties = BlobField(null=True)
    room_name = TextField(null=True)
    service_name = TextField(null=True)
    state = IntegerField(null=True)
    style = IntegerField(null=True)
    successful_query = IntegerField(null=True)

    class Meta:
        db_table = 'chat'

class Handle(BaseModel):
    rowid = PrimaryKeyField(db_column='ROWID', null=True)
    country = TextField(null=True)
    id = TextField()
    service = TextField()
    uncanonicalized = TextField(db_column='uncanonicalized_id', null=True)

    class Meta:
        db_table = 'handle'

class ChatHandleJoin(BaseModel):
    chat = ForeignKeyField(db_column='chat_id', null=True, rel_model=Chat, to_field='rowid')
    handle = ForeignKeyField(db_column='handle_id', null=True, rel_model=Handle, to_field='rowid')

    class Meta:
        db_table = 'chat_handle_join'

class Message(BaseModel):
    rowid = PrimaryKeyField(db_column='ROWID', null=True)
    account = TextField(null=True)
    account_guid = TextField(null=True)
    attributedbody = BlobField(db_column='attributedBody', null=True)
    cache_has_attachments = IntegerField(null=True)
    cache_roomnames = TextField(null=True)
    country = TextField(null=True)
    date = IntegerField(index=True, null=True) # See http://stackoverflow.com/questions/10746562/parsing-date-field-of-iphone-sms-file-from-backup
    date_delivered = IntegerField(null=True)
    date_played = IntegerField(null=True)
    date_read = IntegerField(null=True)
    error = IntegerField(null=True)
    expire_state = IntegerField(index=True, null=True)
    group_action_type = IntegerField(null=True)
    group_title = TextField(null=True)
    guid = TextField(unique=True)
    handle = IntegerField(db_column='handle_id', index=True, null=True)
    # handle = ForeignKeyField(db_column='handle_id', null=True, rel_model=Handle, to_field='rowid')
    has_dd_results = IntegerField(null=True)
    is_archive = IntegerField(null=True)
    is_audio_message = IntegerField(null=True)
    is_auto_reply = IntegerField(null=True)
    is_delayed = IntegerField(null=True)
    is_delivered = IntegerField(null=True)
    is_emote = IntegerField(null=True)
    is_empty = IntegerField(null=True)
    is_expirable = IntegerField(null=True)
    is_finished = IntegerField(null=True)
    is_forward = IntegerField(null=True)
    is_from_me = IntegerField(null=True)
    is_played = IntegerField(null=True)
    is_prepared = IntegerField(null=True)
    is_read = IntegerField(null=True)
    is_sent = IntegerField(null=True)
    is_service_message = IntegerField(null=True)
    is_system_message = IntegerField(null=True)
    item_type = IntegerField(null=True)
    message_action_type = IntegerField(null=True)
    message_source = IntegerField(null=True)
    other_handle = IntegerField(index=True, null=True)
    replace = IntegerField(null=True)
    service = TextField(null=True)
    service_center = TextField(null=True)
    share_direction = IntegerField(null=True)
    share_status = IntegerField(null=True)
    subject = TextField(null=True)
    text = TextField(null=True)
    type = IntegerField(null=True)
    version = IntegerField(null=True)
    was_data_detected = IntegerField(null=True)
    was_deduplicated = IntegerField(null=True)
    was_downgraded = IntegerField(index=True, null=True)

    class Meta:
        db_table = 'message'

class ChatMessageJoin(BaseModel):
    chat = ForeignKeyField(db_column='chat_id', null=True, rel_model=Chat, to_field='rowid')
    message = ForeignKeyField(db_column='message_id', null=True, rel_model=Message, to_field='rowid')

    class Meta:
        db_table = 'chat_message_join'
        primary_key = CompositeKey('chat', 'message')

class DeletedMessages(BaseModel):
    rowid = PrimaryKeyField(db_column='ROWID', null=True)
    guid = TextField()

    class Meta:
        db_table = 'deleted_messages'

class MessageAttachmentJoin(BaseModel):
    attachment = ForeignKeyField(db_column='attachment_id', null=True, rel_model=Attachment, to_field='rowid', primary_key=True)
    # message = ForeignKeyField(db_column='message_id', null=True, rel_model=Message, to_field='rowid')
    message = IntegerField(db_column='message_id', null=True)

    class Meta:
        db_table = 'message_attachment_join'
