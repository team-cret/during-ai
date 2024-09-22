from abc import ABC, abstractmethod

class Reranker:
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def rerank_documents(self, documents):
        pass