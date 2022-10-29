import json
from math import sqrt
import os
import numpy as np
import argparse



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, default='ocr_results.json')
    args = parser.parse_args()
    return args

def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def point(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]

def getAngle2P(p1, p2):  #두점 사이의 각도: 시계 방향으로 계산한다. P1-(0,0)-P2의 각도를 시계방향으로
        ang1 = np.arctan2(*p1[::-1])
        ang2 = np.arctan2(*p2[::-1])
        res = np.rad2deg((ang1 - ang2) % (2 * np.pi))
        if res > 180:
            res = 360 - res
        return res

def wordsize(p1):
    return sqrt(p1[0] ** 2 + p1[1] ** 2)

def dot(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1]

def word_info(words):
    ret_words = []
    for i , word in enumerate(words):
        word_dict = {}
        word_dict['word'] = word['text']
        word_dict['pivot'] = [(word['pos'][0][0] + word['pos'][2][0]) / 2, (word['pos'][0][1] + word['pos'][2][1]) / 2]
        word_dict['width'] = [word['pos'][1][0] - word['pos'][0][0], word['pos'][1][1] - word['pos'][0][1]]
        word_dict['height'] = [word['pos'][3][0] - word['pos'][0][0], word['pos'][3][1] - word['pos'][0][1]]
        word_dict['size'] = wordsize(word_dict['height'])
        word_dict['level'] = 0
        word_dict['num'] = i
        ret_words.append(word_dict)
    return ret_words

def word_combination(words : list, angle_threshold=10, size_threshold=0.5):
    ret_words = []
    checked = set()
    for word in words:
        word_group = []
        if word['num'] in checked :
            continue
        checked.update([word['num']])
        word_group.append(word)
        neighbors = [word]
        while len(neighbors) != 0:
            word = neighbors.pop()
            for i in range(len(words)):
                if not words[i]['num'] in checked and abs(words[i]['size'] - word['size']) < word['size'] * 0.2 :
                    if getAngle2P(point(word['pivot'], words[i]['pivot']), word['width']) < angle_threshold and distance(words[i]['pivot'], word['pivot']) < (wordsize(words[i]['width'])/2 + wordsize(word['width'])/2 + 2*word['size']):
                        new_word = words[i]
                        new_word['level'] = word['level']
                        word_group.append(new_word)
                        checked.update([new_word['num']])
                        neighbors.append(new_word)

                    
                    elif getAngle2P(words[i]['height'], word['height']) < angle_threshold and abs(dot(point(word['pivot'], words[i]['pivot']),word['height'])/word['size']) < 2*word['size'] and distance(words[i]['pivot'], word['pivot']) < max(wordsize(word['width'])/2, wordsize(words[i]['width'])/2):
                        new_word = words[i]
                        if dot(point(word['pivot'], words[i]['pivot']),word['height']) > 0 :
                            new_word['level'] = word['level'] + 1
                        elif dot(point(word['pivot'], words[i]['pivot']),word['height']) < 0 :
                            new_word['level'] = word['level'] - 1
                        word_group.append(new_word)
                        checked.update([new_word['num']])
                        neighbors.append(new_word)
        word_group = sorted(word_group, key=lambda x: x['pivot'][0])
        word_group = sorted(word_group, key=lambda x: x['level'])
        word_group= " ".join([word['word'] for word in word_group])
        ret_words.append(word_group)
    return ret_words


if __name__ == '__main__':
    args = parse_args()
    filename = args.filename
    with open(filename, 'r') as f:
        data = json.load(f)
        new_data = []
        for item in data:
            img_id = item['img_id']

            words = word_info(item['texts'])
            words = word_combination(words)

            new_data.append({'img_id': img_id, 'texts': words})
        with open('ocr_results_combination.json', 'w') as f2:
            json.dump(new_data, f2)
