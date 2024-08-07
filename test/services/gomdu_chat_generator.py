from service.gomdu.chat_generator import ChatGenerator
from model.data_model import GomduChat

class GomduChatGeneratorTester:
    def __init__(self):
        self.setup_for_test()

    def setup_for_test(self):
        self.chat_generator = ChatGenerator()
        self.user_id = 'test_user'
        self.couple_id = 'test_couple'
        self.history_id = 'test_history'

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
            
            gomdu_response = self.chat_generator.generate_next_chat(user_data=user_data)
            print('gomdu response:', gomdu_response)