import nltk

class InputExtractor:
    def __init__(self, n_context=3):
        self.grammar_pattern = r"""
            NP: {<DT|PP\$>?<JJ>*<NN>} # chunk determiner/possessive, adjectives and noun
                {<NNP>} # chunk sequences of proper nouns
        """
        self.chunkerNP = nltk.RegexpParser(self.grammar_pattern)
        self.n_context = n_context
    
    '''
    Method for extracting noun phrases from job_desc input
    '''
    def extractionNP(self, job_desc):
        tagged = self.chunkerNP.parse(nltk.pos_tag(nltk.word_tokenize(job_desc)))
        np_result = []

        for tree in tagged.subtrees(filter=lambda x: x.label() == 'NP'):
            np_result.append(' '.join([child[0] for child in tree.leaves()]))
        for tree in tagged.subtrees(filter=lambda x: x.label() == 'S'):
            np_tags = [child[1] for child in tree.leaves()]
        return np_result, np_tags
    
    '''
    Method for extracting list of contexts (single string) and int (index) of last given phrase
    '''
    def contextExtractionSingle(self, phrase, job_desc, n, tags):
        idx_phrase_char = job_desc.find(phrase)
        job_desc_words = job_desc.split()
        idx_phrase = 0
        
        tags = tags[-len(job_desc_words):]
        x=0
        while(x<idx_phrase_char):
            x += len(job_desc_words[idx_phrase])+1
            idx_phrase += 1
            
        start = idx_phrase - n
        finish = idx_phrase + len(phrase.split()) + n
        if start < 0:
            start = 0
        if finish > (len(job_desc_words)-1):
            finish = len(job_desc_words)
        
        res_context = []
        res_np_tag = []
        res_cox_tag = []
        res_context.append(' '.join(job_desc_words[start:finish]))
        res_np_tag.append(' '.join(tags[idx_phrase:idx_phrase + len(phrase.split())]))
        res_cox_tag.append(' '.join(tags[start:finish]))
        
        return res_context, res_np_tag, res_cox_tag, idx_phrase_char+len(phrase)+1, len(job_desc_words)
    
    '''
    Method for extracting context for each noun phrase and return list of contexts
    '''
    def contextExtraction(self, noun_phrases, job_desc, n, tags):
        context_list = []
        np_tags = []
        cox_tags = []
        last=0
        for phrase in noun_phrases:
            single_context, np_tag, cox_tag, x, job_desc_words = self.contextExtractionSingle(phrase, job_desc[last:], n, tags)
            last += x
            context_list += single_context
            np_tags += np_tag
            cox_tags += cox_tag
        
        return context_list, np_tags, cox_tags
    
    '''
    Method for extracting noun phrases and context of phrases for given job_desc input
    '''
    def extract(self, job_desc):
        noun_phrases, tagged = self.extractionNP(job_desc)
        context, np_tags, cox_tags = self.contextExtraction(noun_phrases, job_desc, self.n_context, tagged)
        
        return noun_phrases, context