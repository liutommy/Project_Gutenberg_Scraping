import requests as req
import os
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO
import re
from time import sleep
from random import uniform

if __name__ == "__main__":
    
    folderPath = "./project_gutenberg"

    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
    }

    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    url = "https://www.gutenberg.org/cache/epub/"

    try:
        res_catlog = req.get(url + "feeds/pg_catalog.csv", headers = my_headers)

        # print(res_catlog.headers)
        # print(res_catlog.content)

        # 如果有連線問題跳出錯誤
        res_catlog.raise_for_status()

        # print("="*50)

        # utf-8-sig解碼中文
        text_catlog = res_catlog.content.decode("utf-8-sig")

        # print(text_catlog)
        # print("="*50)

        # pandas讀取書單csv
        dataframe_catlog =  pd.read_csv(StringIO(text_catlog))

        # print(dataframe_catlog)
        # print("="*50)

    except TimeoutError:
        print("Time out!")

    
    # 讀取中文書單
    dataframe_catlog_zh = dataframe_catlog[dataframe_catlog["Language"] == "zh"]

    # 含有中文的所有書單(txt只有英文)
    # dataframe_catlog[dataframe_catlog["Language"].str.contains(r'zh', regex=True)]

    # 名稱中文含有的所有書單(會選到日文書)
    # dataframe_catlog[dataframe_catlog["Title"].str.contains(r'[\u4e00-\u9fff]', regex=True)]

    # 正規表達式 - 中文與全形標點
    regex_chinese = r"[\u4e00-\u9fff\u3000-\u303F\uFF00-\uFFEF]+"

    # 正規表達式 - 中文與全形標點含空白換行半形非文字
    # regex_chinese = r"[\u4e00-\u9fff\u3000-\u303F\uFF00-\uFFEF\d\s]+"

    for book in dataframe_catlog_zh.itertuples(index=True):

        # 移除書名中的空白字元
        book_name = re.sub(r'\s', '', book[4])
        
        print(f"Text#: {book[1]}, 書名: {book_name}開始下載")

        book_res = req.get(url+ f"{book[1]}/pg{book[1]}.txt")
        
        # 如果有連線問題跳出錯誤
        res_catlog.raise_for_status()

        #解碼中文utf-8-sig
        book_text = book_res.content.decode("utf-8-sig")

        #找出中文與全形標點
        chinese_chars = re.findall(regex_chinese, book_text)

        #組合list
        book_text_chinese = ''.join(chinese_chars)

        with open(f"{folderPath}/{book_name}.txt",  "w", encoding="utf8") as f:
            f.write(book_text_chinese)
        
        print("下載完成")

        #隨機等待1~2秒
        sleep(uniform(1, 2))