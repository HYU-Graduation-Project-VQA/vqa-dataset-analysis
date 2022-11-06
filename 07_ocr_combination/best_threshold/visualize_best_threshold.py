import matplotlib.pyplot as plt
import json

def calculate_score(a, b, c, d, e):
    return ((a * 0 + b * 0.3 + c * 0.6 + d * 0.9 + e)/(a+b+c+d+e))


if __name__ == "__main__":
    scores = object()
    with open("07_ocr_combination/best_threshold/score_distribution.json", "r") as f1:
        scores = json.load(f1)

    scores = scores[0]

    scores_keys = scores.keys()
    scores_keys = list(scores_keys)
    for i in range(len(scores_keys)):
        scores_keys[i] = float(scores_keys[i])
    
    total_scores = list()
    for elem in scores_keys:
        x = scores[str(elem)]
        print(x)
        total_scores.append(calculate_score(x['0'], x['1'], x['2'], x['3'], x['4']))
    
    plt.xlabel("threshold")
    plt.ylabel("total score")
    plt.xticks(scores_keys)
    plt.plot(scores_keys, total_scores)
    print(total_scores)
    plt.show()