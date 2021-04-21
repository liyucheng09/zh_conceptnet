import configparser
import json
import spacy
from spacy.matcher import Matcher
import sys
import timeit
from tqdm import tqdm
import numpy as np
import threading
import os
import pickle

blacklist = set(["-PRON-", "actually", "likely", "possibly", "want",
                 "make", "my", "someone", "sometimes_people", "sometimes","would", "want_to",
                 "one", "something", "sometimes", "everybody", "somebody", "could", "could_be"
                 ])


concept_vocab = set()
config = configparser.ConfigParser()
config.read("paths.cfg")
with open(config["paths"]["concept_vocab"], "r", encoding="utf8") as f:
    cpnet_vocab = [l.strip() for l in list(f.readlines())]
cpnet_vocab = [c.replace("_", " ") for c in cpnet_vocab]
cpnet_vocab=set(cpnet_vocab)

def lemmatize(nlp, concept):

    if '_' not in concept:
        doc=nlp(concept)
        # assert len([token.lemma_ for token in doc])==1, f'bigger than 1 {doc.text}'
        lcs=set()
        lcs.add(''.join([t.lemma_ for t in doc]))
        return lcs

    doc = nlp(concept.replace("_"," "))
    lcs = set()

    # assert len([token.lemma_ for token in doc])==1 , f"bigger than 1 {doc.text}, {'_'.join([token.lemma_ for token in doc])}, {concept}"
    lcs.add("_".join([token.lemma_ for token in doc])) # all lemma
    return lcs

def load_matcher(nlp):

    config = configparser.ConfigParser()
    config.read("paths.cfg")
    matcher_patterns_path=config["paths"]["matcher_patterns"]
    # if os.path.exists(matcher_patterns_path+'.cache'):
    #     with open(matcher_patterns_path+'.cache', 'rb') as f:
    #         matcher=pickle.load(f)
    #     return matcher

    with open(matcher_patterns_path, "r", encoding="utf8") as f:
        all_patterns = json.load(f)

    matcher = Matcher(nlp.vocab)
    for concept, pattern in tqdm(all_patterns.items(), desc="Adding patterns to Matcher."):
        matcher.add(concept, [pattern])
    
    # with open(matcher_patterns_path+'.cache', 'wb') as f:
    #     pickle.dump(matcher, f)
    return matcher

def ground_mentioned_concepts(nlp, matcher, s, ans = ""):
    s = s.lower()
    doc = nlp(s)
    matches = matcher(doc)

    mentioned_concepts = set()
    span_to_concepts = {}

    for match_id, start, end in matches:

        span = doc[start:end].text  # the matched span
        if len(set(span.split(" ")).intersection(set(ans.split(" ")))) > 0:
            continue
        original_concept = nlp.vocab.strings[match_id]

        # if len(original_concept.split("_")) == 1:
        #     original_concept = list(lemmatize(nlp, original_concept))[0]

        if span not in span_to_concepts:
            span_to_concepts[span] = set()

        span_to_concepts[span].add(original_concept)

    for span, concepts in span_to_concepts.items():
        concepts=list(concepts)
        if len(concepts)>1:
            print(f'len>1 *{span} *{"$".join(concepts)}')
            concepts.sort(key=len)
        mentioned_concepts.add(concepts[0])
        # concepts_sorted.sort(key=len)

        # # mentioned_concepts.update(concepts_sorted[0:2])

        # shortest = concepts_sorted[0:3] #
        # for c in shortest:
        #     if c in blacklist:
        #         continue
        #     lcs = lemmatize(nlp, c)
        #     intersect = lcs.intersection(shortest)
        #     if len(intersect)>0:
        #         mentioned_concepts.add(list(intersect)[0])
        #     else:
        #         mentioned_concepts.add(c)
    return mentioned_concepts

def hard_ground(nlp, sent):
    global cpnet_vocab
    sent = sent.lower()
    doc = nlp(sent)
    res = set()
    for t in doc:
        if t.lemma_ in cpnet_vocab:
            res.add(t.lemma_)
    sent = "_".join([t.text for t in doc])
    if sent in cpnet_vocab:
        res.add(sent)
    return res

def match_mentioned_concepts(nlp, sents, answers, matcher, batch_id = -1):
    

    res = []
    # print("Begin matching concepts.")
    for sid, s in tqdm(enumerate(sents), total=len(sents), desc="grounding batch_id:%d"%batch_id):
        a = answers[sid]
        all_concepts = ground_mentioned_concepts(nlp, matcher, s, a)
        answer_concepts = ground_mentioned_concepts(nlp, matcher, a)
        question_concepts = all_concepts - answer_concepts
        if len(question_concepts)==0:
            # print(s)
            question_concepts = hard_ground(nlp, s) # not very possible
        if len(answer_concepts)==0:
            print(a)
            answer_concepts = hard_ground(nlp, a) # some case
            print(answer_concepts)

        res.append({"sent": s, "ans": a, "qc": list(question_concepts), "ac": list(answer_concepts)})
    return res

def process(filename, batch_id=-1):


    nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser', 'textcat'])
    nlp.add_pipe('sentencizer')

    sents = []
    answers = []
    with open(filename, 'r') as f:
        lines = f.read().split("\n")


    for line in tqdm(lines, desc="loading file"):
        if line == "":
            continue
        j = json.loads(line)
        for statement in j["statements"]:
            sents.append(statement["statement"])
        for answer in j["question"]["choices"]:
            answers.append(answer["text"])


    if batch_id >= 0:
        output_path = filename + ".%d.mcp" % batch_id
        batch_sents = list(np.array_split(sents, 100)[batch_id])
        batch_answers = list(np.array_split(answers, 100)[batch_id])
    else:
        output_path = filename + ".mcp"
        batch_sents = sents
        batch_answers = answers

    res = match_mentioned_concepts(nlp, sents=batch_sents, answers=batch_answers, batch_id=batch_id)
    with open(output_path, 'w') as fo:
        json.dump(res, fo)


def load_model_and_matcher():

    if os.path.exists('nlp.cache'):
        with open('nlp.cache', 'rb') as f:
            nlp=pickle.load(f)
    else:
        nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser', 'textcat'])
        nlp.add_pipe('sentencizer')

        with open('nlp.cache', 'wb') as f:
            pickle.dump(nlp, f)

    matcher=load_matcher(nlp)

    return nlp, matcher

def process2(filename):
    
    nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser', 'textcat'])
    nlp.add_pipe('sentencizer')
    matcher = load_matcher(nlp)
    # nlp, matcher = load_model_and_matcher()

    sents = []
    answers = []
    with open(filename, 'r') as f:
        lines = f.read().split("\n")

    for line in tqdm(lines, desc="loading file"):
        if line == "":
            continue
        j = json.loads(line)
        for statement in j["statements"]:
            sents.append(statement["statement"])
        for answer in j["question"]["choices"]:
            answers.append(answer["text"])


    def run(batch_sents, batch_answers, matcher, index):
        # if index == 0: return
        output_path = filename + ".%d.mcp" % index
        res = match_mentioned_concepts(nlp, sents=batch_sents, answers=batch_answers, matcher=matcher, batch_id=index)
        with open(output_path, 'w') as fo:
            json.dump(res, fo)
    
    for index, (batch_sents, batch_answers) in enumerate(zip(np.array_split(sents, 100), np.array_split(answers, 100))):
        # t=threading.Thread(target=run, args=(batch_sents, batch_answers, matcher, index))
        # t.start()
        run(batch_sents, batch_answers, matcher, index)
        

def test():
    nlp = spacy.load('en_core_web_sm', disable=['ner', 'parser', 'textcat'])
    nlp.add_pipe('sentencizer')
    matcher = load_matcher(nlp)
    # nlp, matcher=load_model_and_matcher()
    res = match_mentioned_concepts(nlp, sents=["sammy wanted to go to where the people were.  race track might he go."], answers=["race track"], matcher=matcher)
    print(res)

# "sent": "Watch television do children require to grow up healthy.", "ans": "watch television",
if __name__ == "__main__":
    process2(sys.argv[1])

    # process(sys.argv[1], int(sys.argv[2]))

    # test()