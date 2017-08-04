#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv
import re
import datetime
import run_knp
import prepare_word
import io_word


argvs = sys.argv
argc = len(argvs)

# 引数チェック
if (argc != 3):
    print ('prease type "python %s reviewfile keywordfile"'%argvs[0])
    sys.exit()

if __name__ == "__main__":

    # 入力: レビューファイルの読み込み
    input_f = open(argvs[1])
    Reader_review_data = csv.reader(input_f)
    
    # 入力：キャラクター・キャスト・映画スタッフの読み込み
    input_f = open(argvs[2])
    Reader_keyword_data = csv.reader(input_f)
    keyword_data = [row for row in Reader_keyword_data]

    pn_dic={}
    #入力：日本語評価極性辞書(用語編) 
    with open("./dic/wago.121808.pn",'r') as f:
        for pn_wago in f.readlines():
            pn_wago_tmp = pn_wago.split('\t')

            pn = pn_wago_tmp[0].split('（')[0]
            pn_text = pn_wago_tmp[1].replace(" ","").replace('\n','')
            
            if pn == "ポジ":
                pn_dic[pn_text] = 1
            elif pn == "ネガ":
                pn_dic[pn_text] = -1

    # 入力：日本語評価極性辞書(名詞編)    
    with open("./dic/pn.csv.m3.120408.trim",'r') as f:
        for pn_noun in f.readlines():
            pn_noun_tmp = pn_noun.split('\t')

            if pn_noun_tmp[1] == "p":
                pn_dic[pn_noun_tmp[0]] = 1

            elif pn_noun_tmp[1] == "n":
                pn_dic[pn_noun_tmp[0]] = -1

       
    # 出力：ターゲット単語ごとの係り受け先結果
    output_dic_l = {}
    output_dic_r = {}

    # 出力：レビューごとの係り受け結果(オリジナル)
    file_name1 = "./data/output/result_origin" + str(datetime.datetime.today()) + ".csv"
    output_f1 = open(file_name1, 'w')
    writer1 = csv.writer(output_f1, lineterminator='\n')
    writer1.writerow(["id","keyword","pn","bnst_left","bnst_right","text"])

    # 出力：レビューごとの係り受け結果(係り受けに評価語あり)    
    file_name2 = "./data/output/result_pn" + str(datetime.datetime.today()) + ".csv"
    output_f2 = open(file_name2, 'w')
    writer2 = csv.writer(output_f2, lineterminator='\n')
    writer2.writerow(["id","keyword","pn_word","pn_value","bnst_left","bnst_right","text"])


    
    # レビューデータ分析
    for i,review_data in enumerate(Reader_review_data):

        print(i+1)        
        review_text=re.split(',',review_data[3])
        
        for text in review_text:
            # レビュー文にターゲット単語があるか調べる
            keyword_list = prepare_word.choose_keyword(text,keyword_data) 

            # 記号変換-バグ対策
            symbols = [' ','"']
            for symbol in symbols:
                if symbol in text:
                    text = text.translate(str.maketrans(symbol,"　"))

            # レビュー文にターゲット単語があった場合
            if text != "" and len(keyword_list) != 0:
                #　ターゲット単語・極性語の係り受けid
                for keyword in keyword_list:
                    bnst_dic,keyword_id,pn_list = run_knp.save_bnst(text,keyword,pn_dic)                
                    
                    # 文節ごとに、係り先順を取得
                    bnst_order_dic = run_knp.get_bnst_order(bnst_dic)

                    # ターゲット単語 : 係り受け情報を取得
                    bnst_lefts = run_knp.get_bnst_left(bnst_dic,bnst_order_dic,keyword_id)
                    bnst_right = run_knp.get_bnst_right(bnst_order_dic,keyword_id)
                    
                    result_lefts = [[bnst_dic[i]["word"]  for i in bnst_left ] for bnst_left in bnst_lefts]
                    result_right = [bnst_dic[i]["word"] for i in bnst_right]

                    # ターゲット単語 : 結果書き込み準備                    
                    output_dic_l.setdefault(keyword, []).append(result_lefts)                    
                    output_dic_r.setdefault(keyword, []).append(result_right)
                    
                    
                    # ターゲット係り受けの評価情報出力
                    pn_sum = 0
                    if len(pn_list) != 0:
                        for pn_ids in pn_list:
                            
                            pn_id = pn_ids[0]
                            pn_value = pn_ids[1]

                            pn_sum += pn_value
                            
                            # 左側に評価語あり
                            for bnst_left in bnst_lefts:
                                if pn_id in bnst_left:
                                    # レビューごとの結果書き込み
                                    writer2.writerow([i+1,keyword,"左："+bnst_dic[pn_id]["word"],pn_value,result_lefts,result_right,text])
                                    
                            # 右側に評価語あり
                            if pn_id in bnst_right:                                                                
                                # レビューごとの結果書き込み                            
                                writer2.writerow([i+1,keyword,"右:"+bnst_dic[pn_id]["word"],pn_value,result_lefts,result_right,text])
                                
                    # レビューごとの結果書き込み(+評価あり)
                    writer1.writerow([i+1,keyword,pn_sum,result_lefts,result_right,text])

            
    # ターゲット単語ごとの結果書き込み
    io_word.write_csv(output_dic_l,"./data/output/target_l")
    io_word.write_csv(output_dic_r,"./data/output/target_r")


    input_f.close()
    output_f1.close()
    output_f2.close()

   
