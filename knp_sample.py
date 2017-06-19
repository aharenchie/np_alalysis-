#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from pyknp import KNP


"""
構文解析結果を保存

in：評価極性語,評価極性語のある文章
out:構文解析結果の辞書

"""
def save_bnst_info(pn_word,text):        

    bnst_dic ={}    
    pn_id = 0
 
    child_list=[]
    parent_list=[]

    # 1. 構文結果を保存 (1.親id辞書,2.単語id辞書) 
    knp = KNP()
    result = knp.parse(text)

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

    return bnst_dic,pn_id


"""
評価極性語の係り元を取得
in：評価極性語,評価極性語のある文章
out:構文解析結果の辞書(方向は複数ある)  
"""
def get_bnst_child(bnst_dic,pn_id):
    serch_ids = [pn_id]
    flag = True
    child_list =[]
    match = 0

    while flag:
        match = 0
        next_ids = []
        
        for serch_id in serch_ids:        
            for key,value in bnst_dic.items():
                if value["parent_id"] == serch_id:
                    child_list.append([key,value["word"]])
                    next_ids.append(key)
                    match += 1
                
        if match == 0:
            flag = False

        serch_ids = next_ids
        print(serch_ids)

    
    return child_list
                            
"""
評価極性語の係り先を取得
in：評価極性語,評価極性語のある文章
out:構文解析結果の辞書(方向は一つ)
"""

def get_bnst_parent(bnst_dic):

    bnst_dic_parent={}
        
    for my_id in bnst_dic.keys():

        flag = True
        parent_list=[]
        serch_id = my_id
        
        while flag:
            parent_id = bnst_dic[serch_id]["parent_id"]
            
            if parent_id != -1:
                parent_list.append(bnst_dic[parent_id]["word"])
            else:
                flag = False

            serch_id = parent_id

        bnst_dic_parent[my_id]  = parent_list

    return bnst_dic_parent  

    
if __name__ == '__main__' :

    bnst_dic = {}

    
    #text = "ミャハの不思議なカリスマ性が上田さん声で表現されていて素晴らしいです"
    #pn_word = "ミャハ"
    text="アニメ映画としては何がいいのかわからない作品でした"
    pn_word = "いい"
    
    bnst_dic,pn_id = save_bnst_info(pn_word,text)
    bnst_dic_parent = get_bnst_parent(bnst_dic)
    child_list = get_bnst_child(bnst_dic,pn_id) 
    print("ターゲット単語: {0}".format(pn_word))
    print("入力文章: {0}".format(text))
    print("-----------------------")
    print("ターゲット単語に係り先: {0}".format(bnst_dic_parent[pn_id]))
    print("ターゲット単語に係るもの：{0}".format(child_list))

