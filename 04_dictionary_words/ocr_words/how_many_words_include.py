import json
import tqdm

'''
    OCR로 만들어진 단어들이 얼마나 많이 기존 word list에 있는지 확인해보고자 한다.
    이때 combination algorithm으로 만들어진 단어들은 모두 띄어쓰기 단위로 떼어내고 개별적으로 본다.
    결과물: OCR 단어 중 word list에 포함된 단어 개수
    기준: str1 in str2.split(" ")
    결과: JSON 및 개수 --> 969개

'''

WORDS_JSON = "04_dictionary_words/ocr_words/trainval_ans2label.json"
OCR_WORDS = "04_dictionary_words/ocr_words/ocr_words.json"


if __name__ == '__main__':
    words_json = object()
    ocr_words = object()
    
    with open(WORDS_JSON, 'r') as f:
        words_json = json.load(f)
    with open(OCR_WORDS, 'r') as f:
        ocr_words = json.load(f)
    
    words_json = list(words_json.keys())
    ocr_words = ocr_words["words"]
    how_many_words_include_result = list()
    
    wordListOCR = set()
    
    for word in tqdm.tqdm(ocr_words):
        word_ = word.split(" ")
        for word__ in word_:
            wordListOCR.add(word__)
    
    for word in wordListOCR:
        if word in words_json:
            how_many_words_include_result.append(word)
    
    print("the number of words that OCR_words IN words_list: ", len(how_many_words_include_result))
    
    how_many_words_include_result = {"words": how_many_words_include_result}
    
    with open("04_dictionary_words/ocr_words/how_many_words_include_result.json", "w") as fp:
        json.dump(how_many_words_include_result, fp, indent=4) 