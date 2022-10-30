import json
import tqdm

qid_json = object()
with open('09_improvement_test_2/results/qids_question_type.json', 'r') as f:
    qid_json = json.load(f)

results = dict()

qtypes = list(qid_json.keys())

for qtype in tqdm.tqdm(qtypes):
    qids = qid_json[qtype]
    for qid in qids:
        results[str(qid)] = qtype

with open('09_improvement_test_2/results/qid_qtype.json', 'w') as fp:
    json.dump(results, fp, indent=4)