import json

QUESTION_JSON = 'val2014_json/v2_OpenEnded_mscoco_val2014_questions.json'

if __name__ == '__main__':

    qids = list()

    with open(QUESTION_JSON) as f1:
        question_json = json.load(f1)
    
    for elem in question_json['questions']:
        qids.append(elem['question_id'])
    
    qids.sort()

    # print(qids)

    # how to save or read?
    '''
        https://stackoverflow.com/questions/27745500/how-to-save-a-list-to-a-file-and-read-it-as-a-list-type
    '''

    with open('results/val2014_qids.json', 'w') as fp:
        json.dump(qids, fp)
    
    # when read -> with open("", "rb") as fp:
    #               b = json.load(fp)