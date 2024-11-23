from flask import Flask, request, redirect, render_template
import subprocess
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('sd5_input_form.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    crop = request.form.get('crop1')
    area = request.form.get('area1')
    workers = request.form.get('labor')

    # Pythonスクリプトを実行
    command = f"python3 wp/agriculture_scraper.py {crop} {area} {workers}"
    subprocess.run(command, shell=True)

    return redirect('/results')

@app.route('/results') #FIXME23~29行目の部分は、データベースからデータを取得してリザルトページに表示するコードとなっていますが、いるかいらないかわからない上に直接データベースにアクセスする形になってしまってると思うので、できれば編集願いたいです。
def results():
    conn = sqlite3.connect('probc_sd5.db')
    c = conn.cursor()
    c.execute("SELECT * FROM crops")
    crops = c.fetchall()
    conn.close()

    return render_template('sd5_result.html', crops=crops)

if __name__ == '__main__':
    app.run(debug=True)