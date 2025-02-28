import os, sys
import logging

def init_setting() -> None:
    # path setting
    #----------------------------------------------------------------------#
    try:
        dir_path = os.path.abspath(os.path.dirname('during-ai'))
        sys.path.insert(0, dir_path)
        print('success path registration [dir-path] :', dir_path)
    except Exception:
        print('failed to register path')
        logging.error('exception occurred', exc_info=True)
    #----------------------------------------------------------------------#

    # api key setting
    #----------------------------------------------------------------------#
    try:
        from setting.env_setting import EnvSetting
        api_key_setter = EnvSetting()
        api_key_setter.set_api_key()
    except Exception:
        print('failed to set api key')
        logging.error('exception occurred', exc_info=True)
    #----------------------------------------------------------------------#