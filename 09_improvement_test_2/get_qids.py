import json
import tqdm


QUESTION_TYPE = [
    'what number is',
    'what is the name',
    'what time',
    'why',
    'why is the',
    'what does the',
    'where is the',
    'how',
    'where are the',
    'what brand',
    'who is',
    'which',
    'what',
    'what is on the',
    'what is the',
    'what type of',
    'what is',
    'what are the',
    'what kind of',
    'what is in the',
    'how many'
]

qid_basket = {
    'what number is': [],
    'what is the name': [],
    'what time': [],
    'why': [],
    'why is the': [],
    'what does the': [],
    'where is the': [],
    'how': [],
    'where are the': [],
    'what brand': [],
    'who is': [],
    'which': [],
    'what': [],
    'what is on the': [],
    'what is the': [],
    'what type of': [],
    'what is': [],
    'what are the': [],
    'what kind of': [],
    'what is in the': [],
    'how many': []
}

ANNOTATION_FILE = 'val2014_json/v2_mscoco_val2014_annotations.json'

annotation_file = object()
with open(ANNOTATION_FILE, 'r') as f1:
    annotation_file = json.load(f1)
annotation_file = annotation_file["annotations"]

for q in tqdm.tqdm(annotation_file):
    if q['question_type'] in QUESTION_TYPE:
        qid_basket[q['question_type']].append(q['question_id'])

with open('09_improvement_test_2/results/qids_question_type.json', 'w') as fp:
    json.dump(qid_basket, fp, indent=4)