import json

with open('v2_OpenEnded_mscoco_train2014_questions.json') as f:
    jsonData = json.load(f)

    questions = jsonData["questions"]
    q_dict = {}
    for elem in questions:
        if( elem['question'] not in q_dict):
            q_dict[elem['question']] = {'nums': 1, 'images': []}
            q_dict[elem['question']]['images'] = [elem['image_id']]
        else:
            q_dict[elem['question']]['nums'] += 1
            q_dict[elem['question']]['images'].append(elem['image_id'])
    
    # for elem in q_dict:
    #     if q_dict[elem]["nums"] == 111:
    #         print(elem, q_dict[elem])

    over_2_dict = dict(filter(lambda elem:elem[1]['nums']>=2, q_dict.items()))
    # print(over_2_dict)

    with open("more_than_two_questions.json", "w") as fp:
        json.dump(q_dict,fp) 