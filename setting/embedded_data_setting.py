
import numpy as np
import os, sys

dir_path = os.path.abspath(os.path.dirname('during-ai'))
sys.path.insert(0, dir_path)
print('successfully inserted path')
print('dir_path : ', dir_path)

from setting.api_key_setting import APIKeySetting
api_key_setter = APIKeySetting()
api_key_setter.set_api_key()

from ai_model.embedding.gemini import GeminiTextEmbedding
from ai_model.embedding.ko_sroberta import KoSrobertaTextEmbedding
from ai_model.embedding.upstage import UpstageTextEmbedding
from ai_model.embedding.openai import OpenAITextEmbedding
from ai_model.embedding.text_embedding import TextEmbedding
from data.sentiments import sentiments, sentiment_to_id
from model.ai_model import AIModelInfo
from setting.config import Config
from setting.model_config import ModelConfig

embedding_models = {
    'gemini' : GeminiTextEmbedding(AIModelInfo(
                api_key_name=Config.GOOGLE_API_KEY.value,
                ai_model_id=ModelConfig.GEMINI_EMBEDDING_MODEL_ID.value,
                ai_model_name=ModelConfig.GEMINI_EMBEDDING_MODEL_NAME.value
            )),
    'ko_sroberta' : KoSrobertaTextEmbedding(AIModelInfo(
                    ai_model_name=ModelConfig.KO_SROBERTA_EMBEDDING_MODEL_NAME.value
            )),
    'upstage' : UpstageTextEmbedding(AIModelInfo(
                    ai_model_name=ModelConfig.UPSTAGE_EMBEDDING_MODEL_NAME.value
            )),
    'openai' : OpenAITextEmbedding(AIModelInfo()),
}

def save_embedded_data() -> None:
    for model_name, model in embedding_models.items():
        model: TextEmbedding
        embedded_data = {}
        for sentiment_id, value in sentiments.items():
            sentiment = value['sentiment']

            embedded_vector = model.embed_text(sentiment)
            embedded_data[str(sentiment_id)] = embedded_vector
        print(model_name, type(model_name))
        np.savez(f'data/embedded_data/{model_name}.npz', **embedded_data)
        print(f'successfully saved {model_name} embedded vectors')
    print('successfully saved all embedded vectors')

def load_embedded_data() -> None:
    for model_name in embedding_models.keys():
        embedded_data = np.load(f'data/embedded_data/{model_name}.npz')

        embedded_sentiments = {}
        for key, value in embedded_data.items():
            embedded_sentiments[int(key)] = value
        print(embedded_sentiments.keys())
        print(f'successfully loaded {model_name} embedded vectors')

load_embedded_data()