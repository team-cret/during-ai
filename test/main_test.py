import init_setting

class Tester:
    def __init__(self) -> None:
        init_setting.init_setting()
        self.setup_for_test()
    
    def setup_for_test(self):
        from unit import embedding_model
        from unit import classification_model
        self.test_setup = {
            'embedding_model'      : [False, embedding_model.EmbeddingModelTester()],
            'classification_model' : [False, classification_model.ClassificationModelTester()],
        }

    def test(self):
        for do_test, tester in self.test_setup.values():
            if do_test:
                tester.test()

tester = Tester()
tester.test()