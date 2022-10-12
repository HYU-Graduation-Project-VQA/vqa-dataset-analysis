import json
import tqdm

# multiple_choice_answer에 나온 단어가
# dictionary에 없는 경우가 있는지를 조사하고자 함.

with open('dictionary_words/dictionary_txt.json', 'r') as f:
    data = json.load(f)

words = data.keys()

with open('val2014_json/v2_mscoco_val2014_annotations.json') as f:
    annotation_file = json.load(f)

annotation_file = annotation_file['annotations']

not_in_words = set()

for elem in tqdm.tqdm(annotation_file):
    answer = elem['multiple_choice_answer']
    word_list = answer.split(" ")
    for word in word_list:
        if word not in words:
            not_in_words.add(word)

not_in_words = {'words': list(not_in_words)}

with open('not_in_words.json', 'w') as fp:
    json.dump(not_in_words, fp)