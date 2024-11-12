from sentence_transformers import SentenceTransformer

class KoE5TextEmbedding:
    def __init__(self):
        self.set_model()

    def set_model(self):
        self.model = SentenceTransformer("nlpai-lab/KoE5")

    def embed_text(self, text:str) -> list[float]:
        return self.model.encode(['query: ' + text])[0]

    def embed_text_list(self, texts:list[str]) -> list[list[float]]:
        texts = ['passage: ' + text for text in texts]
        return self.model.encode(texts)

    def similarity(self, embeddings1: list[float], embeddings2: list[float]) -> float:
        return self.model.similarity(embeddings1, embeddings2)