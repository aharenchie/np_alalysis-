#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from pyknp import KNP


"""
構文解析結果を取得

in：評価極性語,評価極性語のある文章
out:親単語

"""
def get_bnst_info(pn_word,text):        

    bnst_dic ={}
    
    pn_id = 0
    pn_par_id = 0

    child_list=[]
    parent_list=[]
    
    knp = KNP()
    result = knp.parse(text)

    # 1. 構文結果を保存 (1.親id辞書,2.単語id辞書) 
    for bnst in result.bnst_list():
        word = ""
        dic_value ={}

        # 1-1.単語の結合、評価極性語のidの調査
        for mrph in bnst.mrph_list():            

            if mrph.midasi == pn_word: 
                pn_id = bnst.bnst_id
                
            word += mrph.midasi 

        # 1-2.辞書追加
        dic_value["parent_id"] = bnst.parent_id
        dic_value["word"]= word

        bnst_dic[bnst.bnst_id] = dic_value
        
    # 2. 

        
    # 3. 評価極性語の係り元を調査
    serch_id = pn_id
    while True:
        pn_par_id = bnst_dic[serch_id]["parent_id"]
        
        if pn_par_id == -1:
            break
        else:
            parent_list.append(bnst_dic[pn_par_id]["word"])
            
        serch_id = pn_par_id
        
    print(bnst_dic)
    print(child_list)
    print(parent_list)
    print(pn_id)


if __name__ == '__main__' :

    bnst_dic = {}
    
    text = "太郎はきれいな花子が読んでいる本を次郎に渡した"
    pn_word = "読んで"
    get_bnst_info(pn_word,text)
    

