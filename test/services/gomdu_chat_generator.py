from model.data_model import GomduChat

from service.gomdu.gomdu import Gomdu

class GomduChatGeneratorTester:
    def __init__(self):
        self.setup_for_test()

    def setup_for_test(self):
        self.gomdu = Gomdu()
        self.user_id = 'test_user'
        self.couple_id = 'test_couple'
        self.history_id = 'test_history'

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
            
            user_data = GomduChat(
                user_id='test_user',
                couple_id='test_couple',
                message=user_message,
                timestamp=0
            )
            
            gomdu_response = self.gomdu.generate_next_chat(user_data=user_data)
            print('gomdu response:', gomdu_response)