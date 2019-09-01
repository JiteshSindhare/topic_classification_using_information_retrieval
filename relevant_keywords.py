import json
import requests
"""
References
API- http://www.datamuse.com/api/
stopwords-  https://gist.github.com/sebleier/554280
handling json- https://realpython.com/python-json/

"""



datamuse_api_url="https://api.datamuse.com/words"

related_synonym="?rel_syn=" # synonyms
related_triggered="?rel_trg=" # triggered means statistically associated with the querry word
related_kind_of="?rel_spc=" #"Kind of" (direct hypernyms, per WordNet)	gondola → boat
related_general="?rel_gen=" # "More general than" (direct hyponyms, per WordNet)	boat → gondola
related_comprises="?rel_com=" # 	"Comprises" (direct holonyms, per WordNet)	car → accelerator
related_part_of="?rel_par=" # "Part of" (direct meronyms, per WordNet)	trunk → tree
related_frequent_follower="?rel_bga=" #Frequent followers (w′ such that P(w′|w) ≥ 0.001,per Google Books Ngrams)wreak → havoc
related_frequent_predecesor="?rel_bgb="#Frequent predecessors (w′ such that P(w|w′) ≥ 0.001, per Google Books Ngrams)havoc → wreak
queries=[related_comprises, related_general, related_kind_of, related_part_of, related_synonym,
           related_triggered]
more_queries = [related_comprises, related_general, related_kind_of, related_part_of, related_synonym,
           related_triggered,related_frequent_follower,related_frequent_predecesor
           ]

stop_wrds=[]
with open('stopwords.txt','r') as rf:
    for count,line in enumerate(rf):
        stop_wrds.append(line.strip('\n'))

class Relavant_keywords:

    def __init__(self):
        self.key =''
    def save_result(self, result):
        """
        this method is used by other method to generate file of related words
        :param result: data we recieved from API
        :return: generates file
        """
        words_inserted = []
        with open('keywords/{}.txt'.format(self.key), 'a') as fi:
            if self.key not in words_inserted:
                fi.write(self.key)
                fi.write('\n')
                words_inserted.append(self.key)
            for res in result:
                if res['word'] not in stop_wrds and len(res['word'])>2:
                    fi.write(res['word'])
                    words_inserted.append(res['word'])
                    fi.write('\n')

    def related_words(self,key):
        """
        :param key: word/words/topic name which we want to find related keywords for
        :return: it does not return anything but invokes a method which
        creates file with relevant keywords in /keywords directory
        """
        self.key=key
        for i in queries:
            requests_queries = requests.get(datamuse_api_url+i+key)
            data=json.loads(requests_queries.text)
            self.save_result(data)

    def more_related_keywords(self,key):
        """
        difference between this one and related_words is it uses some more queries to find keywords ,
        this one can be used when not enough words were found using related_words
        :param key: word/words/topic name which we want to find related keywords for
        :return: it does not return anything but invokes a method which
        creates file with relevant keywords in /keywords directory
        """
        self.key=key
        for i in more_queries:
            requests_queries = requests.get(datamuse_api_url+i+key)
            data=json.loads(requests_queries.text)
            self.save_result(data)

    def custom_keywords(self,key,filename):
        """
        when not enough words can be found using above two methods then this method can be used with more comples queries
        :param key: it contains custom querry for any keyword like what to write after"words" in the link below
         https://api.datamuse.com/words
        :param filename: what should be the name of topic for which keywords we are finding
        :return: it does not return anything but invokes a method which
            creates file with relevant keywords in /keywords directory
        """
        self.key=filename
        requests_queries=requests.get(datamuse_api_url+key)
        data=json.loads(requests_queries.text)
        self.save_result(data)

keywords=Relavant_keywords()
#keywords.more_related_keywords("Export")
#keywords.related_words('linear_regression')
#keywords.custom_keywords("?rel_trg=livestock&topics=export","Livestock export")
keywords.custom_keywords("?rel_trg=linear&topics=regression","Linear regression")
