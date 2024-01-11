from app.models.models import Role
from app.security.passwd_cryptography import encrypt_pass
from .db import USERS_DATA


USERS_DATA['foo'] = {'login': 'foo', 'password': encrypt_pass('TEST1234'), 'role': Role.ADMIN}
USERS_DATA['bar'] = {'login': 'bar', 'password': encrypt_pass('test5678'), 'role': Role.USER}
USERS_DATA['baz']= {'login': 'baz', 'password': encrypt_pass('TeSt1234'), 'role': Role.GUEST}