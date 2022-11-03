import json
import tqdm

'''
    ocr_results_combination.json은 COCO 데이터셋 이미지에서 OCR을 실행시켜 인식된 단어들을
    이미지 id별로 저장한 후 combination 알고리즘을 적용한 결과이다.
    
    위의 과정으로 만들어진 단어 리스트를 중복 없이 모아 하나의 JSON 파일로 만들고자 한다.
    ** OCR 결과 중 단어 개수(중복X)
    the number of words:  29764
    
'''

OCR_WORDS_JSON = "07_ocr_combination/ocr_results_combination.json"

if __name__ == "__main__":
    ocr_words = set()
    
    ocr_json = object()
    with open(OCR_WORDS_JSON, 'r') as f:
        ocr_json = json.load(f)
    
    for img in tqdm.tqdm(ocr_json):
        words = img["texts"]
        for word in words:
            ocr_words.add(word)
    
    print('the number of words: ', len(ocr_words))
    
    ocr_words_dict = {"words": list(ocr_words)}
    
    with open("04_dictionary_words/ocr_words/ocr_words.json", "w") as fp:
        json.dump(ocr_words_dict,fp) 