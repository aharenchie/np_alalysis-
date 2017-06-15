
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import re
import types
import MeCab

"""
1.辞書の読み込み
in : なし
out : 評価極性辞書 dic

やること：DB機能の実装
"""
def import_pn_data():

    pn_dic ={}

    # 1-2.日本語評価極性辞書(用語編)
    with open("/Users/e125731/workspace/m1/dic/wago.121808.pn",'r') as f:
        for pn_wago in f.readlines():
            pn_wago_list = pn_wago.split('\t')
        
            # 評価用言の変換
            pn_wago_list[1] = pn_wago_list[1].replace(" ","").replace('\n','')

            # ネガポジの数値化
            value_list = pn_wago_list[0].split('（')
            if value_list[0] == "ポジ":
                value = 1 #ポジ
            else:
                value = -1 #ネガ

            # 辞書に追加
            pn_dic[pn_wago_list[1]] = value



    # 1-3.日本語評価極性辞書(名詞編)
    with open("/Users/e125731/workspace/m1/dic/pn.csv.m3.120408.trim",'r') as f:

        # ネガポジの数値化
        for pn_noun in f.readlines():
            pn_noun_list = pn_noun.split('\t')
            if pn_noun_list[1] == "p":
                value = 1 #ポジ
            elif pn_noun_list[1] == "n":
                value = -1 #ネガ
            elif pn_noun_list[1] == "e":
                value = 0 #ニュートラル

            # 辞書に追加
            pn_dic[pn_noun_list[0]] = value

    return(pn_dic)

"""
2.レビューデータ形態素解析
in : 1件のレビューデータ str
out : 1件のレビューデータの分かち書き list

やること：ストップワードの追加
"""
def import_review_data(text):
    word_list = []
    mt = MeCab.Tagger("-Ochasen -d /usr/local/Cellar/mecab/0.996/lib/mecab/dic/mecab-ipadic-neologd")
    mt.parse('')
    node = mt.parseToNode(text)
    
    while node:
        if node.feature.split(",")[0] != "BOS/EOS":
            word_list.append(node.surface)
        node = node.next

    return(word_list)

"""
 3.文章（単語リスト）に対する評価極性値を返す。
in : 1件のレビューデータ list
out : 1件レビューデータ評価極性値 int, 評価極性語 list


"""
def cal_review_pn(word_list):
    p_word=[]
    n_word=[]
    e_word=[]
    score = 0
    
    for word in word_list:
        
        if word in pn_dic:
            score += pn_dic[word]
            
            if pn_dic[word] == 1:
                p_word.append(word)
            elif pn_dic[word] == 0:
                e_word.append(word)
            elif pn_dic[word] == -1:
                n_word.append(word)

    return(score,p_word,e_word,n_word)
            

if __name__ == "__main__":

    argvs = sys.argv
    argc = len(argvs)

    if (argc != 2):
        print ('prease type "python %s reviewfile"'%argvs[0])
        sys.exit()

    # 辞書の読み込み
    pn_dic = import_pn_data()
    
    # レビューの読み込み
    f = open(argvs[1])
    dataReader_review = csv.reader(f)

    compare_data = {}

    # レビュー評価計算
    for review in dataReader_review:

        user_score = re.search(r'[0-9]+',review[1]).group()
        text = review[2]

        # レビューデータの形態素解析
        word_list = import_review_data(text)
        # 評価極性値の計算
        score,p_word,e_word,n_word = cal_review_pn(word_list)

        print(text)        
        print("")
        print("ユーザー評価 予想評価")
        print("{0}            {1}".format(user_score,score))
        print("ポジティブ単語:{0}".format(p_word))
        print("ネガティブ単語:{0}".format(n_word))
        print("ニュートラル単語:{0}".format(e_word))
        print("---------------------------")

        compare_data.setdefault(user_score, []).append(score)

    # 比較出力用
    for key, value in compare_data.items():
        print("ユーザー評価 予想評価")
        print("{0}            {1}".format(key,value))

         
        
            
