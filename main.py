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

    # 出力：ターゲット単語ごとの係り受け先結果
    output_dic_l = {}
    output_dic_r = {}

    # 出力：レビューごとの係り受け結果
    file_name = "./data/output/result" + str(datetime.datetime.today()) + ".csv"
    output_f = open(file_name, 'w')
    writer = csv.writer(output_f, lineterminator='\n')
    writer.writerow(["id","keyword","text","bnst_left","bnst_right"])
    
    for i,review_data in enumerate(Reader_review_data):

        print(i+1)

        review_text=re.split('[,。]',review_data[3])
        
        for text in review_text:
            keyword_list = prepare_word.choose_keyword(text,keyword_data)

            text = text.replace(" ","　")


            if text != "" and len(keyword_list) != 0:

                for keyword in keyword_list:
                    bnst_dic,keyword_id = run_knp.save_bnst(keyword,text)
                
                    # 文節ごとに、係り先順を取得
                    bnst_order_dic = run_knp.get_bnst_order(bnst_dic)

                    # ターゲット単語が受けるものを取得
                    bnst_left = run_knp.get_bnst_left(bnst_dic,bnst_order_dic,keyword_id)
            
                    # ターゲット単語が係るものを取得
                    bnst_right = run_knp.get_bnst_right(bnst_dic,bnst_order_dic,keyword_id)
                    
                    # ターゲット単語ごとの結果書き込み準備
                    output_dic_l.setdefault(keyword, []).append(bnst_left)
                    output_dic_r.setdefault(keyword, []).append(bnst_right)

                    # レビューごとの結果書き込み
                    writer.writerow([i+1,keyword,text,bnst_left,bnst_right])

    # ターゲット単語ごとの結果書き込み
    io_word.write_csv(output_dic_l,"./data/output/target_l")
    io_word.write_csv(output_dic_r,"./data/output/target_r")


    input_f.close()
    output_f.close()
    


    
