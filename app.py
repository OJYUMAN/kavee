from flask import Flask,render_template,request
import ssg
from checksound import*

app = Flask(__name__)

@app.route('/', methods=['GET'])
def drop():
    types = ['กาพย์', 'กลอน', 'โคลง', 'ฉันท์' ,'ร่าย']
    return render_template('index.html', types=types)

@app.route('/')
def index() :
    return render_template("index.html")


"""
ฉันเดินไปที่ครัวเมื่อเช้านี้
พบคุณพี่เล่นเกมอย่างสุขสันต์
มาเมื่อไรก็พบทุกคืนวัน
เลยมาเล่นด้วยกันอยู่บ่อยครั้ง
"""

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text'] #รับtextจากindex
    text = text.split("\r\n") #ตัดวรรค
    text2 = [ssg.syllable_tokenize(a) for a in text]#ตัดเป็นคําในวรรคอีกที
    text3 = []#สร้างarrayเป็นตัวเช็คคําถูกผิด >>>> [0,1]
    for i in range(len(text2)):#สร้าง []
        text3.append([])
        for m in range(len(text2[i])):#ใส่ 0 ใน []
            text3[i].append(0)


    for b in range(len(text)):
        if rhyme((text2[b])[-1]) != rhyme((text2[1])[2]):
            if rhyme((text2[0])[-1]) != rhyme((text2[1])[4]):
                (text3[0])[-1] = 1
                (text3[1])[2] = 1
                (text3[1])[4] = 1

        if rhyme((text2[1])[-1]) != rhyme((text2[2])[-1]):
            (text3[1])[-1] = 1
            (text3[2])[-1] = 1

        if rhyme((text2[2])[-1]) != rhyme((text2[3])[2]):
            if rhyme((text2[2])[-1]) != rhyme((text2[3])[4]):
                (text3[2])[-1] = 1
                (text3[3])[2] = 1
                (text3[3])[4] = 1





    return render_template("rhyme.html",text=text2, text3=text3)


if __name__ == "__main__":
    app.run(debug=True)

