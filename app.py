from flask import Flask, render_template, request
import ssg
from checksound import *
from ojsound import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep


app = Flask(__name__)

@app.route('/', methods=['GET'])
def drop():
    types = ['กลอนสุภาพ','กาพย์ยานี ๑๑',"กาพย์ฉบัง ๑๖"]
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
    type = request.form['types']
    print(type)
    text3 = [] #สร้างarrayเป็นตัวเช็คคําถูกผิด >>>> [0,1]
    for i in range(len(text2)): #สร้าง []
        text3.append([])
        for m in range(len(text2[i])):#ใส่ 0 ใน []
            text3[i].append(0)

    if type == "กลอนสุภาพ":
        file = open("chantaluck/klorn8.txt", "r")
    elif type == "กาพย์ยานี ๑๑":
        file = open("chantaluck/kapyanee11.txt", "r")
    elif type == "กาพย์ฉบัง ๑๖":
        file = open("chantaluck/chabung16.txt", "r")
    chant = file.read()
    chant = chant.split("\n")
    print(chant)

    bote = len(chant) #จำนวนวรรคในบท
    r = len(text2) #จำนวนวรรค
    r = r/bote #จำนวนบท
    newchant = [x.split(",") for x in chant]
    if r != int(r):
        return render_template("rhyme.html", text=["วรรคไม่ครบบท"], text3=[1])
    # วรรคครบ
    r = int(r)
    wannayuk = []
    for x in newchant:
        wannayuk.append(x[-1])
        del x[-1]
    print(text2)
    print(newchant)
    listofrhymeindex = [{} for x in range(5)]
    dictofp={}
    for wak, wakl in enumerate(newchant):
        for payang, word in enumerate(wakl):
            if word == wakl[-1]:
                pp = -1
            else:
                pp = payang
            if any(x in word for x in [str(y) for y in range(1, 6)]):
                if wak not in listofrhymeindex[int(word.replace("/", "").replace("p", ""))-1]:
                    listofrhymeindex[int(word.replace("/", "").replace("p", ""))-1][wak] = [pp]
                else:
                    listofrhymeindex[int(word.replace("/", "").replace("p", "")) - 1][wak].append(pp)
            if 'p' in word:
                if dictofp == {}:
                    dictofp[wak] = [pp]
                else: dictofp[wak-bote] = [pp]
    lir = [a for a in listofrhymeindex if a != {}] #list_index_rhyme
    print(lir)
    print(dictofp)
    listtofind = [dict(x) for x in lir]
    for key,value in dictofp.items():
        for rhymeind in lir:
            if any(set(value).issubset(set(v)) and k==key for k, v in rhymeind.items()):
                for kk,vv in dictofp.items():
                    if kk not in rhymeind.keys():
                        rhymeind[kk]=[]
                    if not any(ww in rhymeind[kk] for ww in vv):
                        (rhymeind[kk]).extend(vv)
    print(listtofind)
    print(lir)
    for c in range(1,r):
        fiib = c*bote #first index in bote
        for x in lir:
            dicty = dict()
            for y,val in x.items():
                dicty[y+fiib] = val
            listtofind.append(dicty)
    print(listtofind)
    for ll in listtofind:
        boolee = True
        torhyme = rhyme(text2[list(ll.keys())[0]][list(ll.values())[0][0]])
        for x,y in ll.items():
            boolee = boolee and any(rhyme(text2[x][z]) == torhyme for z in y)
        if not boolee:
            for x,y in ll.items():
                for z in y:
                    text3[x][z] = 1


    return render_template("rhyme.html",text=text2, text3=text3)


@app.route('/submit2', methods=['POST'])
def submit2():
    text = request.form['text']
    text2 = ssg.syllable_tokenize(text)
    text44 = text2[-1]

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://rhymethai.com")
    driver.find_element(By.NAME, 'inputword').send_keys(text44)#พิมขื่อ
    driver.find_element(By.CSS_SELECTOR, '.btn:not(:disabled):not(.disabled)').click()#กดค้นหา
  #a = driver.find_element(By.CLASS_NAME, "card-body")


    soup = BeautifulSoup(driver.page_source)#ดึงหน้าwebมา
    element = soup.find(class_="text-center")#ตัดชื่อเว็บ
    element.decompose()
    element2 = soup.find(class_="form-inline justify-content-center")#ตัดปุ่มค้นหาของเว็บ
    element2.decompose()
    soup = soup.find(class_="card-body")#เอาแค่ส่วนเนื้อหา
    #page = soup.getText("\n\r")


    return render_template("index.html", text=text, texty=soup)

if __name__ == "__main__":
    app.debug=True
    app.run()



"""
from flask import Flask, render_template, request
import ssg
from checksound import *
from ojsound import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep







app = Flask(__name__)


@app.route('/', methods=['GET'])
def drop():
  types = ['กลอนสุภาพ']
  return render_template('index.html', types=types)


@app.route('/')
def index():
  return render_template("index.html")



ฉันเดินไปที่ครัวเมื่อเช้านี้
พบคุณพี่เล่นเกมอย่างสุขสันต์
มาเมื่อไรก็พบทุกคืนวัน
เลยมาเล่นด้วยกันอยู่บ่อยครั้ง

แล้วสอนว่าอย่าไว้ใจมนุษย์
มันแสนสุดลึกล้ำเหลือกำหนด
เหมือนเถาวัลย์พันเกี่ยวที่เลี้ยวลด
ก็ไม่คนเหมือนหนึ่งในน้ำใจ



@app.route('/submit', methods=['POST'])
def submit():
  text = request.form['text']  #รับtextจากindex
  text = text.split("\r\n")  #ตัดวรรค
  text2 = [ssg.syllable_tokenize(a) for a in text]  #ตัดเป็นคําในวรรคอีกที
  ##print(text2)
  text3 = []  #สร้างarrayเป็นตัวเช็คคําถูกผิด >>>> [0,1]
  for i in range(len(text2)):  #สร้าง []
    text3.append([])
    for m in range(len(text2[i])):  #ใส่ 0 ใน []
      text3[i].append(0)

  r = len(text2)
  r = int(r / 4)

  for b in range(r):

    c = 4 * b
    if rhyme((text2[c])[-1]) != rhyme((text2[c + 1])[2]):
      if rhyme((text2[c])[-1]) != rhyme((text2[c + 1])[4]):
        (text3[c])[-1] = 1
        (text3[c + 1])[2] = 1
        (text3[c + 1])[4] = 1

    if rhyme((text2[c + 1])[-1]) != rhyme((text2[c + 2])[-1]):
      (text3[c + 1])[-1] = 1
      (text3[c + 2])[-1] = 1

    if rhyme((text2[c + 2])[-1]) != rhyme((text2[c + 3])[2]):
      if rhyme((text2[c + 2])[-1]) != rhyme((text2[c + 3])[4]):
        (text3[c + 2])[-1] = 1
        (text3[c + 3])[2] = 1
        (text3[c + 3])[4] = 1

    arr1 = [[c, -1], [c, -1], [c + 1, -1], [c + 2, -1], [c + 2, -1],
            [c + 1, -1], [c + 1, -1]]
    arr2 = [[c + 1, 2], [c + 1, 4], [c + 2, -1], [c + 3, 2], [c + 3, 4],
            [c + 3, 2], [c + 3, 4]]
    for x in range(len(arr1)):
      x1 = arr1[x]
      x2 = arr2[x]
      if text2[x1[0]][x1[1]] == text2[x2[0]][x2[1]]:
        text3[x1[0]][x1[1]] = 2
        text3[x2[0]][x2[1]] = 2

  for a in range(r):
    b = 4 * a + 1
    if b != 1:
      if rhyme(text2[b][-1]) != rhyme(text2[b - 2][-1]):
        text3[b][-1] = 1
        text3[b - 2][-1] = 1

  return render_template("rhyme.html", text=text2, text3=text3)


@app.route('/submit2', methods=['POST'])
def submit2():
  text = request.form['text']
  text2 = ssg.syllable_tokenize(text)
  text44 = text2[-1]

  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get("http://rhymethai.com")
  driver.find_element(By.NAME, 'inputword').send_keys(text44)#พิมขื่อ
  driver.find_element(By.CSS_SELECTOR, '.btn:not(:disabled):not(.disabled)').click()#กดค้นหา
  #a = driver.find_element(By.CLASS_NAME, "card-body")


  soup = BeautifulSoup(driver.page_source)#ดึงหน้าwebมา
  element = soup.find(class_="text-center")#ตัดชื่อเว็บ
  element.decompose()
  element2 = soup.find(class_="form-inline justify-content-center")#ตัดปุ่มค้นหาของเว็บ
  element2.decompose()
  soup = soup.find(class_="card-body")#เอาแค่ส่วนเนื้อหา
  page = soup.getText("\n\r")


  return render_template("index.html", text=text, texty=page)







if __name__ == "__main__":
  app.debug = True
  #app.run(host="0.0.0.0", port=5000)
  app.run()
"""
