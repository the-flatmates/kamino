from typing import List

import gensim.downloader
import numpy as np
import spacy

nlp = spacy.load("en_core_web_lg")
corpus = gensim.downloader.load("glove-wiki-gigaword-300")


def pair_similarity(token1: str, token2: str) -> float:
    """Compute similarity between two tokens.

    Args:
        token1 (str): First token
        token2 (str): Second token

    Returns:
        float: Similarity score
    """
    tokens = nlp(" ".join([token1, token2]))
    return tokens[0].similarity(tokens[1])


def pairwise_similarity(word: str, words: List[str]) -> List[float]:
    """Compute pairwise similarity between a word and a word list.

    Args:
        word (str): Word to compute pairwise similarity with
        words (List[str]): Word list to compare

    Returns:
        List[float]: Similarity scores
    """
    word_token = nlp(word)
    wl_tokens = nlp(" ".join(words))

    similarities = []

    for wl_token in wl_tokens:
        similarities.append(word_token.similarity(wl_token))

    return similarities


def group_similarity(words: List[str]) -> float:
    """Compute average similarity among list of words.

    Args:
        words (list): List of words.

    Returns:
        float: Similarity score
    """
    tokens = nlp(" ".join(words))

    similarities = []

    for i, i_token in enumerate(tokens):
        for j, j_token in enumerate(tokens):
            if i <= j:
                continue

            similarities.append(i_token.similarity(j_token))

    return sum(similarities) / len(similarities)


def most_similar(words: list, count: int = 1) -> List[str]:
    """Get the most similar words to given list of words.

    Args:
        words (list): List of words.
        count (int, optional): Number of similar words to return. Defaults to 1.

    Returns:
        List[str]: List of similar words.
    """
    tokens = nlp(" ".join(words))

    avg_vector = [0] * 300
    for token in tokens:
        avg_vector += token.vector

    ms = nlp.vocab.vectors.most_similar(np.asarray([avg_vector]), n=count)
    return [str(nlp.vocab.strings[w]) for w in ms[0][0]]


def wv_most_similar(positive: list, negative: list = [], count: int = 5) -> List[str]:
    """Get the top N most similar words.

    Args:
        positive (list): Words that contribute positively towards similarity.
        negative (list, optional): Words that contribute negatively towards similarity. Defaults to [].
        count (int, optional): Number of words to return. Defaults to 5.

    Returns:
        List[str]: List of similar words.
    """

    return corpus.most_similar(positive=positive, negative=negative, topn=count)
