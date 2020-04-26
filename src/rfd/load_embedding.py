import numpy as np
from tqdm import tqdm
def load_embedding(vocabulary_size, tokenizer, embedding_size=100):
    """
        This function loads the pretrained embedding into a embedding matrix
        Parameters:
            vocabulary_size: size of the vocabulary
            tokenizer: tokenizer object
            embedding_size: size of the embedding vector (for 100 100d glove vector)
        Returns: embedding matrix
    """
    embeddings_index = dict()
    f = open('../embeddings/glove.6B.100d.txt', encoding='utf8')
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()
    embedding_matrix = np.zeros((vocabulary_size, embedding_size))
    for word, index in tqdm(tokenizer.word_index.items()):
        if index > vocabulary_size - 1:
            break
        else:
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[index] = embedding_vector

    return embedding_matrix