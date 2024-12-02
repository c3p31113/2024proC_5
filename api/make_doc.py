import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Wordファイルを開く
try:
    doc = docx.Document("Test.docx")  # ファイル名とパスを正確に指定
except FileNotFoundError:
    print("ファイルが見つかりません。ファイル名やパスを確認してください。")
    exit()
except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit()

def replace(len:int, old_text:str, new_text:str):
    rep = doc.paragraphs[len]
    t = rep.text
    t = t.replace(old_text, new_text)
    rep.text = t
    return

# 表の中の文字を置き換える
def table_replace(old_text:str, new_text:str):
    for table in doc.tables:  # 文書内のすべての表をループ
        for row in table.rows:  # 各表のすべての行をループ
            for cell in row.cells:  # 各行のすべてのセルをループ
                # 結合されたセルの最初のセルでのみテキストを置き換え
                if cell.text and old_text in cell.text:  # テキストが空でない場合に置き換え
                    cell.text = cell.text.replace(old_text, new_text)
    return

# print("段落の個数:", len(doc.paragraphs))

print("表の個数:", len(doc.tables))

# # Docファイルの内容を表示
# num = 0
# for para in doc.paragraphs:
#     num = num + 1
#     print(num, para.text)

# 日付編集
replace(3, "yyyy", "2021")
replace(3, "mm", "6")
replace(3, "dd", "04")

#住所追加
para = doc.paragraphs[5]
para.insert_paragraph_before("申請者住所　伊達市〇〇町１２３－４")
#右揃えがしたかったができなかった↓
doc.paragraphs[5].alignment = WD_ALIGN_PARAGRAPH.RIGHT
# 名前
replace(7, "姓名", "文教太郎")

# 誕生日年齢
replace(8, "yyyy", "2004")
replace(8, "mm", "10")
replace(8, "dd", "15")
replace(8, "age", "20")

#法人設立年月日
replace(9, "yyyy", "2024")
replace(9, "mm", "4")
replace(9, "dd", "1")

#農業経営開始
replace(9, "yyyy", "2024")
replace(9, "mm", "4")
replace(9, "dd", "1")

# ここから下は表

# 農業経営開始日
table_replace("yyyy", "2026")
table_replace("mm", "4")
table_replace("dd", "1")

# tbl = doc.tables[0]
# for row in tbl.rows:
#     row_text = []
#     for cell in row.cells:
#         row_text.append(cell.text)
#     # print(row_text)
#     print("".join(row_text).replace("\u3000", "_"))

# 別名保存
doc.save("Result.docx")

# 保存後のファイル中身確認
try:
    doc = docx.Document("Result.docx")  # ファイル名とパスを正確に指定
except FileNotFoundError:
    print("ファイルが見つかりません。ファイル名やパスを確認してください。")
    exit()
except Exception as e:
    print(f"エラーが発生しました: {e}")
    exit()