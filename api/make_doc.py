from docx import Document
from docx.document import Document as DocumentObject
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime
from os import makedirs


def open_docx(path: str) -> DocumentObject:
    try:
        doc = Document(path)  # ファイル名とパスを正確に指定
    except FileNotFoundError:
        print("ファイルが見つかりません。ファイル名やパスを確認してください。")
        exit()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit()
    return doc


# Wordファイルを開く
doc = open_docx("api/Test.docx")


def replace(len: int, old_text: str, new_text: str):
    rep = doc.paragraphs[len]
    t = rep.text
    t = t.replace(old_text, new_text)
    rep.text = t
    return


# 表の中の文字を置き換える
def table_replace(old_text: str, new_text: str):
    for table in doc.tables:  # 文書内のすべての表をループ
        for row in table.rows:  # 各表のすべての行をループ
            for cell in row.cells:  # 各行のすべてのセルをループ
                # 結合されたセルの最初のセルでのみテキストを置き換え
                if (
                    cell.text and old_text in cell.text
                ):  # テキストが空でない場合に置き換え
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
dt_now = datetime.datetime.now()
replace(3, "yyyy", str(dt_now.year))
replace(3, "mm", str(dt_now.month))
replace(3, "dd", str(dt_now.day))

# 行を挿入して文字を入力する例（５行目に新たな行を挿入し、データを入力する）
# para = doc.paragraphs[5]
# para.insert_paragraph_before("申請者住所　伊達市〇〇町１２３－４")
# doc.paragraphs[5].alignment = WD_ALIGN_PARAGRAPH.RIGHT


# ここから下は表

# tbl = doc.tables[0]
# for row in tbl.rows:
#     row_text = []
#     for cell in row.cells:
#         row_text.append(cell.text)
#     # print(row_text)
#     print("".join(row_text).replace("\u3000", "_"))

makedirs("tmp/", exist_ok=True)

# 別名保存
doc.save("tmp/Result.docx")
print("./tmp/Result.docx に保存")

# 保存後のファイル中身確認
doc = open_docx("tmp/Result.docx")  # ファイル名とパスを正確に指定
