from flask import Flask,render_template,request
import ssg
from checksound import*

app = Flask(__name__)


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

    if (text2[0])[-1] != (text2[0])[2] or (text2[0])[4]:
        (text3[0])[-1] = 1
        (text3[1])[2] = 1
        (text3[1])[4] = 1

    #(text3[0])[0]=1
    print(rhyme((text2[0])[0]))
    #oksound((text2[0])[0])
    #print(len(text2))
    #print(text2)
    #T1 = "".join(text2[0])
    #T2 = "".join(text2[1])
    #T3 = "".join(text2[2])
    #T4 = "".join(text2[3])

    #print((text2[1])[2])
    return render_template("rhyme.html",text=text2, text3=text3)


if __name__ == "__main__":
    app.run(debug=True)

