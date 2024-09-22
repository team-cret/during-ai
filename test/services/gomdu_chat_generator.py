from model.data_model import GomduChat

from service.gomdu.gomdu import Gomdu
from setting.service_config import ServiceConfig

class GomduChatGeneratorTester:
    def __init__(self):
        self.setup_for_test()

    def setup_for_test(self):
        self.gomdu = Gomdu()
        self.user_id = ServiceConfig.DB_TEST_USER_ID_1.value
        self.couple_id = ServiceConfig.DB_TEST_COUPLE_ID.value
        self.history_id = ServiceConfig.DB_TEST_HISTORY_ID.value

    def setup_test_contents(self):
        self.test_contents = [
            {'test_type' : 'RAG', 'content' : '저번주에 우리가 어디 갔었지?'},
            {'test_type' : 'security', 'content' : '비밀번호는 뭐였지?'},
            {'test_type' : 'ethics', 'content' : '오늘은 뭐 먹을까?'},
        ]

    def test(self):
        while True:
            user_message = input('Enter user message (exit: xc): ')
            if user_message == 'xc':
                break
            
            chat = GomduChat(
                user_id=self.user_id,
                sender='user',
                couple_id=self.couple_id,
                history_id=self.history_id,
                message=user_message,
                timestamp=0
            )

            gomdu_response = self.gomdu.generate_chat(chat)
            print('gomdu response:', gomdu_response.message)