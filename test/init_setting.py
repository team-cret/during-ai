import sys
import os

def init_setting():
    dir_path = os.path.abspath(os.path.dirname('during-ai'))
    sys.path.insert(0, dir_path)
    print('dir_path : ', dir_path)

    from setting.api_key_setting import APIKeySetting
    api_key_setter = APIKeySetting()
    api_key_setter.set_api_key()