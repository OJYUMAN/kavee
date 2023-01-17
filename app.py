from flask import Flask,render_template,request
import ssg

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
    #text=request.args.get("text")
    text = request.form['text']
    text=text.split("\r\n")
    text2 = [ssg.syllable_tokenize(a) for a in text]
    return render_template("rhyme.html",text=text2)


if __name__ == "__main__":
    app.run(debug=True)
