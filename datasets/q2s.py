import spacy

class QueryConverter:

    def __init__(self, name="en_core_web_sm"):
        self.nlp=spacy.load(name)
        self.wh_words = ["which", "what", "where", "when", "how", "who", "why"]
        self.blank_str = '[BLANK]'

    def get_fitb(self, sents):
        docs = list(self.nlp.pipe(sents))
        templates = []

        for doc in docs:
            wh_words = self._wh_finder(doc)

            if len(wh_words)>1:
                wh_word = self._choice_one_wh(wh_words)
            else:
                wh_word = wh_words[0]
            
            template = self._produce_fitb(doc, wh_word)
            templates.append(template)
        
        return templates
    
    def _produce_fitb(self, doc, wh_word):
        """
        产出一个fill-in-the-blank模版，现阶段方法只能靠规则判断了。

        """

        tokens = [i for i in doc]

        if wh_word.lemma_ in ['what', 'which', 'who']:
            if doc[wh_word.i + 1].dep_ in ['aux', 'auxpass']:
                aux = doc[wh_word.i + 1]
                subj = None
                if doc[wh_word.i + 1].lemma_ != 'do':
                    subj = self._find_the_nearest_subj(doc, wh_word.i + 2)
                tokens.remove(wh_word)
                tokens.remove(aux)

                blank_insert_index = tokens.index(wh_word.head) + 1
                tokens.insert(blank_insert_index, '___')

                if subj is not None:
                    aux_insert_index = tokens.index(subj) + 1
                    tokens.insert(aux_insert_index, aux)
                
                return ' '.join([i.text if not isinstance(i, str) else i for i in tokens])
            else:
                return self._replace_wh_with_blank_directly(doc, wh_word)
        
        if wh_word.lemma_ in ['where', 'when', 'how', 'why']:
            if wh_word.dep_ in ['ccomp', 'pcomp', 'xcomp']:
                return self._replace_wh_with_blank_directly(doc, wh_word)
            elif wh_word.dep_ in ['advmod']:
                if doc[wh_word.i + 1].dep_ in ['aux', 'auxpass', 'ROOT']:
                    aux = doc[wh_word.i + 1]
                    if doc[wh_word.i + 1].lemma_ != 'do':
                        subj = self._find_the_nearest_subj(doc, wh_word.i + 2)
                    tokens.remove(wh_word)
                    tokens.remove(aux)

                    place_for_advmod = self._place_for_advmod(doc, wh_word, type='end_of_sent')
                    blank_insert_index = tokens.index(place_for_advmod) + 1 if place_for_advmod.dep_ != 'punct' else tokens.index(place_for_advmod)
                    prep = self._get_prep_for_advmod(doc, wh_word)
                    tokens.insert(blank_insert_index, prep+' ___')

                    if subj is not None:
                        aux_insert_index = tokens.index(subj) + 1
                        tokens.insert(aux_insert_index, aux)
                    
                    return ' '.join([i.text if not isinstance(i, str) else i for i in tokens])
                else:
                    return self._replace_wh_with_blank_directly(doc, wh_word)
    
    def _place_for_advmod(self, doc, wh_word, type='subtree'):
        if type == 'subtree':
            return list(wh_word.head.subtree)[-1]
        elif type == 'end_of_sent':
            return doc[-1]
    
    def _find_the_nearest_subj(self, doc, start):
        while doc[start].dep_ != 'nsubj' and start < len(doc):
            start+=1
        if start>=len(doc):
            return None
        return doc[start]
    
    def _get_prep_for_advmod(self, doc, wh_word):
        if wh_word.lemma_ == 'where':
            return 'in'
        elif wh_word.lemma_ == 'why':
            return 'because'
        elif wh_word.lemma_ == 'when':
            return 'at'
        elif wh_word.lemma_ == 'how':
            return 'by'
        raise ValueError()
    
    def _replace_wh_with_blank_directly(self, doc, wh_word):
        return doc.text[:wh_word.idx] + '___' + doc.text[wh_word.idx+len(wh_word):]

    def _wh_finder(self, doc):
        
        whs = []
        for token in doc:
            if token.lemma_ in self.wh_words:
                whs.append(token)
        return whs

    def _choice_one_wh(self, wh_words):
        wh_words.reverse()

        for t in wh_words:
            if t.lemma_ == 'what':
                return t
        
        for t in wh_words:
            if t.lemma_ == 'where':
                return t
        return wh_words[0]

if __name__ == '__main__':
    test_cases=['What do you call the caretakers of a child?',
    'Where would you run in to a niece you only see every one and a while?',
    'What uses a ribbon to put words on paper?',
    'Where are sheep likely to live?']
    converter = QueryConverter()
    print(converter.get_fitb(test_cases))