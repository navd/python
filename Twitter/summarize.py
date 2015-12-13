#!/usr/bin/env python3.4

import os
import random
from collections import Counter

from nltk.tokenize.regexp import WordPunctTokenizer

nltk_tokenizer = WordPunctTokenizer()


def tokenize(text):
    return nltk_tokenizer.tokenize(text.lower())


def loadcorpus():
    """Load the corpus of abstracts and documents."""
    dirname = "cmplg-txt"
    abstracts = {}
    documents = {}
    for fn in sorted(os.listdir(dirname)):
        docid = fn.split("-")[0]
        if fn.endswith("abstract.txt"):
            with open(os.path.join(dirname, fn), 'r') as f:
                abstracts[docid] = f.read()
        if fn.endswith("sentences.txt"):
            with open(os.path.join(dirname, fn), 'r') as f:
                documents[docid] = f.readlines()
    return abstracts, documents


def summarize_random(sentences, k, **kwargs):
    """This is a summarizer that returns k random sentences."""
    summary_sentences = random.sample(sentences, k)
    return "\n".join(summary_sentences)


def summarize_initial(sentences, k, **kwargs):
    """This is a summarizer that returns the first k sentences from the
    document.

    """
    summary_sentences = []
    for i in range(k):
        summary_sentences.append(sentences[i])
    #
    # Add your code here
    #
    # This should be pretty straightforward.
    # If you need a refresher on Python's slice notation, see:
    # http://www.diveintopython.net/native_data_types/lists.html
    #
    return "\n".join(summary_sentences)


def summarize_frequency(sentences, k, **kwargs):
    """This is a summarizer that ranks sentences based on their word
    frequencies..

    """
    summary_sentences = []

    # Tokenize each sentence, and keep track of each token's frequency
    word_freqs = Counter()
    for sentence in sentences:
        for token in tokenize(sentence):
            word_freqs[token] += 1

    # Assign a score to each sentence:
    sent_scores = []
    for sentence in sentences:
        score = 0
        for word in tokenize(sentence):
            score += word_freqs[word]
        sent_scores.append(score)

    # Get the top-ranked sentences
    top_sentences = sorted(zip(sent_scores, sentences), reverse=True)
    for i in range(k):
        summary_sentences.append(top_sentences[i][1])
    
    return "\n".join(summary_sentences)


def summarize_other(sentences, documents, k, **kwargs):
    """This is a custom summarizer.

    """
    summary_sentences = []
    nu_of_sentences = 0
    # Tokenize each sentence, and keep track of each token's frequency
    word_freqs = Counter()
    for sentence in sentences:
        nu_of_sentences += 1
        for token in tokenize(sentence):
            word_freqs[token] += 1

    # Assign a score to each sentence:
    sent_scores = []
    for sentence in sentences:
        score = 0
        for word in tokenize(sentence):
            score += word_freqs[word]
        sent_scores.append(score)

    # Get the top-ranked sentences
    top_sentences = sorted(zip(sent_scores, sentences), reverse=True)
    #from_index = (nu_of_sentences - k)
    for i in range(4, k + 6):
        summary_sentences.append(top_sentences[i][1])
    return "\n".join(summary_sentences)


def generate_summaries(summarizer, documents, **kwargs):
    """Use the given summarizer to create summaries for all the
    documents. The summaries are saved to files in the output
    directory.

    """
    if not os.path.exists("output"):
        os.makedirs("output")
    for docid in documents.keys():
        summary = summarizer(
            sentences=documents[docid],
            documents=documents,
            **kwargs)
        fn = "{:s}-{:s}.txt".format(docid, summarizer.__name__)
        print("Writing {:s}".format(fn))
        with open(os.path.join("output", fn), "w") as f:
            f.write(summary)
    return


def main():
    
    # K is the number of sentences to include in the summary
    k = 5
    
    abstracts, documents = loadcorpus()
    print("{:d} abstracts loaded.".format(len(abstracts)))
    print("{:d} documents loaded.".format(len(documents)))

    # Create the summaries
    for summarizer in [
            summarize_initial,
            summarize_random,
            summarize_frequency,
            summarize_other,
    ]:
        generate_summaries(summarizer, documents, k=k)

    return


if __name__ == '__main__':
    main()
