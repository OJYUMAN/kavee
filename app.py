from flask import Flask,render_template,request
import ssg
from checksound import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def drop():
    types = ['กลอนสุภาพ']
    return render_template('index.html', types=types)

@app.route('/')
def index() :
    return render_template("index.html")


"""
ฉันเดินไปที่ครัวเมื่อเช้านี้
พบคุณพี่เล่นเกมอย่างสุขสันต์
มาเมื่อไรก็พบทุกคืนวัน
เลยมาเล่นด้วยกันอยู่บ่อยครั้ง

แล้วสอนว่าอย่าไว้ใจมนุษย์
มันแสนสุดลึกล้ำเหลือกำหนด
เหมือนเถาวัลย์พันเกี่ยวที่เลี้ยวลด
ก็ไม่คนเหมือนหนึ่งในน้ำใจ
"""

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text'] #รับtextจากindex
    text = text.split("\r\n") #ตัดวรรค
    text2 = [ssg.syllable_tokenize(a) for a in text] #ตัดเป็นคําในวรรคอีกที
    print(text2)
    text3 = [] #สร้างarrayเป็นตัวเช็คคําถูกผิด >>>> [0,1]
    for i in range(len(text2)): #สร้าง []
        text3.append([])
        for m in range(len(text2[i])):#ใส่ 0 ใน []
            text3[i].append(0)

    r = len(text2)
    r = int(r/4)

    for b in range(r):

        c=4*b
        if rhyme((text2[c])[-1]) != rhyme((text2[c+1])[2]):
            if rhyme((text2[c])[-1]) != rhyme((text2[c+1])[4]):
                (text3[c])[-1] = 1
                (text3[c+1])[2] = 1
                (text3[c+1])[4] = 1

        if rhyme((text2[c+1])[-1]) != rhyme((text2[c+2])[-1]):
            (text3[c+1])[-1] = 1
            (text3[c+2])[-1] = 1

        if rhyme((text2[c+2])[-1]) != rhyme((text2[c+3])[2]):
            if rhyme((text2[c+2])[-1]) != rhyme((text2[c+3])[4]):
                (text3[c+2])[-1] = 1
                (text3[c+3])[2] = 1
                (text3[c+3])[4] = 1

        arr1=[[c,-1],[c,-1],[c+1,-1],[c+2,-1],[c+2,-1],[c+1,-1],[c+1,-1]]
        arr2=[[c+1,2],[c+1,4],[c+2,-1],[c+3,2],[c+3,4],[c+3,2],[c+3,4]]
        for x in range(len(arr1)):
            x1 = arr1[x]
            x2 = arr2[x]
            if text2[x1[0]][x1[1]] == text2[x2[0]][x2[1]]:
                text3[x1[0]][x1[1]] = 2
                text3[x2[0]][x2[1]] = 2

    for a in range(r):
        b=4*a+1
        if b != 1:
            if rhyme(text2[b][-1]) != rhyme(text2[b-2][-1]):
                text3[b][-1] = 1
                text3[b-2][-1] = 1







    return render_template("rhyme.html",text=text2, text3=text3)


if __name__ == "__main__":
    app.run(debug=True)

