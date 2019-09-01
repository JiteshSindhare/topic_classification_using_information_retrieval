import os
import math

"""Reference
implementing tf-idf-
    https://www.freecodecamp.org/news/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3/
getting path to parent directory-
    https://www.tutorialspoint.com/How-do-I-get-the-parent-directory-in-Python
    https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python/7166139
iterating file of a current directory-
    https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
removing punctuation & extra chars- 
    https://www.researchgate.net/post/How_can_you_remove_full-stops_hashtags_symbols_commas_hyphen_semicolon_etc_from_dataset_using_python_for_sentiment_analysis2

"""




class tf_idf:

    def __init__(self):
        self.doc_and_word_frequency = {}
        # related key lists contains list of all the words as value contains in a file , filename is key
        # is of form dict of dict. i.e. related_key_lists[key:filename]=(value:list of all words in that file)
        self.related_key_lists = {}

        # contains term frequency in the form
        """tf[key:filename]=(value:
                    ( dict[key:terms in that file]=val:frequency score of the term )
                    )"""
        self.tf = {}
        # contains inverse document frequency in same form as tf.
        self.idf = {}

    def remove_extras(self,s1):
        check = """#!,()\/.-;'+=$%^&*@/1234567890?><][{}":\n\t"""
        make_string = ''
        for char in s1:
            if (char not in check):
                make_string += char
            elif char == '\n':
                make_string += ' '
        return make_string

    def name_of_highest_score_topic(self,score):
        # to get the name of document which has highest score
        sort_key = 0
        sort_val = 0
        for key, val in score.items():
            if score[key] > sort_val:
                sort_key = key
                sort_val = score[key]
        return sort_key
    def get_topic(self,name):
        """
        :param name: name of file in the form as filename.txt, and file should be in folder summaries
        :return: return name of the topic of that file
        """
        filename="summaries/"+name
        file_path = os.path.dirname(os.path.dirname(__file__))
    # Collecting stopwords in a list, so as avoid adding them in dict/list
        stop_words = []
        path_to_stopwords = os.path.abspath(os.path.join(file_path, 'stopwords.txt'))
        with open(path_to_stopwords) as f:
            for count, line in enumerate(f):
                stop_words.append(line.strip('\n'))
    # get a string of contents of file we want topic for with its special characters removed.
        make_string = ''
        with open(filename) as file:
            for line in file:
                make_string += self.remove_extras(line)


        lis_of_words = make_string.split(' ')# contains words of our target file but contains stop_words
        refine_words = []  # contains words of our target file with stop_words removed
        for w in lis_of_words:
            if w not in stop_words:
                refine_words.append(w)


        #words_set = set(refine_words)
        # dictionary of each terms frequency in target document
        """probably of no use for now
        count_words = dict.fromkeys(refine_words, 0)
        for word in refine_words:
            count_words[word] += 1
        """

        df = dict.fromkeys(refine_words, 0)


        path_to_topics = os.path.abspath(os.path.join(file_path, 'keywords'))
        for files in os.listdir(path_to_topics):
            if files.endswith('.txt'):
                with open(path_to_topics + '\\' + files) as f:
                    strings1 = ''
                    for line in f:
                        strings1 += self.remove_extras(line)
                    self.related_key_lists[files] = strings1.split(' ')



        # frequency of words present in document we are checking vs  related keyword document
        for key, val in self.related_key_lists.items():
            freq = dict.fromkeys(self.related_key_lists[key], 0)
            for words in refine_words:
                if words in self.related_key_lists[key]:
                    freq[words] += 1
            self.doc_and_word_frequency[key] = freq

        # calculate  term frequency- (number of times that term appeared in document / total number of words)
        for key, val in self.related_key_lists.items():
            #N = len(self.related_key_lists[key])  # total number of words or terms in a document
            N = len(refine_words)  # total number of words or terms in a document
            freq = {}
            for word, coun in self.doc_and_word_frequency[key].items():
                freq[word] = float(coun / N)
            self.tf[key] = freq


        # calculating df (document frequency)- number of documents in our collection that contain term t
        for key, val in self.related_key_lists.items():
            for words in set(refine_words):
                if words.lower() in self.related_key_lists[key]:
                    df[words] += 1

        # calculating idf(term)- log(N/df[term]) where N is total number of documents
        for key, val in self.related_key_lists.items():
            freq = {}
            N = len(self.related_key_lists) # Total number of document (topics we have to choose from)
            for word, coun in self.doc_and_word_frequency[key].items():
                if word in df.keys():
                    freq[word] = float(math.log(N / df[word]))
            self.idf[key] = freq

        # print("TERM FREQUENCY", self.tf)
        # print("idf", self.idf)

        #initializing score variable which will contain key as name of document , value as score of document
        score = dict.fromkeys(self.related_key_lists.keys(), 0)
        print('score before calculating',score)
        # calculating final score of each document , sum of tf[term]*idf[term] for each non zero term of every document
        for key, val in self.related_key_lists.items():
            temp_score = 0
            tf_by_doc = self.tf[key]
            idf_by_doc = self.idf[key]
            for key2, val2 in self.idf[key].items():
                temp_score += float(tf_by_doc[key2]) * float(idf_by_doc[key2])
            score[key] = temp_score


        print('score after calculating',score)

        name=self.name_of_highest_score_topic(score)
        #print(sort_key)
        return name[:-4]


topic=tf_idf()
#filename='summaries/random_finance.txt'
filename='unknown1.txt'
Topic=topic.get_topic(filename)
print(Topic)
