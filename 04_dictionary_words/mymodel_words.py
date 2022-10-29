import pickle
# import cPickle
import json

with open('dictionary_words/dictionary.pkl', 'rb') as f:
    data = pickle.load(f)

WORDS = dict(data[0])
WORDS = WORDS.keys()

ANSWER_JSON = 'val2014_json/val_answer.json'
with open(ANSWER_JSON) as f1:
    result_json = json.load(f1)

word_dict = set()

for answers in result_json:
    words = answers["answer"].split(" ")
    for word in words:
        word_dict.add(word)

i = 0
for words in word_dict:
    if words not in WORDS:
        i += 1
        print(words)
print(i)
# data = dict(data[0])
# for elem in data.keys():
#     # elem[0].isalpha() or not elem[-1].isalpha()
#     if ':' in elem:
#         print(elem)


# with open('dictionary_words/dictionary_txt.txt', 'w') as f1:
#     for elem in data:
#         f1.write(str(elem))
    
#     f1.close()

# def load_from_file(cls, path):
#         print('loading dictionary from %s' % path)
#         word2idx, idx2word = cPickle.load(open(path, 'rb'))
#         d = cls(word2idx, idx2word)
#         return d