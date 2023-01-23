import pythainlp
from pythainlp.corpus.common import thai_words, thai_syllables, thai_negations, thai_stopwords, thai_family_names, thai_female_names, thai_male_names, countries, provinces
from ssg import syllable_tokenize
import re


tu = str.maketrans("มวกขฃคฅฆงยญณนฎฏดตศษสบปพภผฝฟหอฮจฉชซฌฐฑฒถทธรฤลฦ"
                   ,"mw111111g233344444445555666666777778888889999")

tu2 = str.maketrans("ะัาิีึืุูเแโอยำใไว็"
                   ,"abcdefghijklmnopqrs")


#data0 = list(thai_words()) + list(thai_syllables()) + list(thai_negations()) + list(thai_stopwords()) + list(thai_family_names()) + list(thai_female_names()) + list(thai_male_names()) + list(countries()) + list(provinces())
data0 = list(thai_words()) + list(thai_syllables())
text = input("text =")
data = []
datas = []
vw = ""
i2 = []
# data0 = list of all words
# text = input
# others will be used later

def cutword():
    # to only use the last syllable of the word cutting all syllables before
    # ปฏิบัติ -> บัติ, ตำรวจ -> รวจ (ไม่ได้เช็คว่าถูกหมดไหม)
    for x in data0:
        w = syllable_tokenize(x)
        w = str(w[-1])
        #print(w)
        data.append(w)
    # then the last syllables are kept in "data"

def convertdata():
    # change "data" to phonetic form and cut the front letter then keep it in "datas"
    global data
    y = ""
    for x in data:
        y = rhyme(x)
        datas.append(y)


def find():
    # find all words that match the phonetic form
    # the words are kept in indeces in "i2" and will be used to display in show()
    global datas
    global i2
    i = 0
    for x in datas:
        if z == x:
            #print(z,i)
            i2.append(i)
        i += 1


def show():
    # print the indeces kept in i2
    global i2
    for x in i2:
        print(data0[x])

def rhyme(s):
    global y, x

    s = re.sub('รร([เ-ไ])', 'ัน\\1', s)  # 4. รร แล้วตามด้วยสระ เ แ โ ไ เปลี่ยน รร เป็น ั น
    s = re.sub('รร([ก-ฮ])', 'ั\\1', s) # 5. ถ้า รร แล้วต่อด้วยพยัญชนะ เปลี่ยน รร เป็นสระ ั
    s = re.sub('รร([ก-ฮ][ะ-ู่-์])','ัน\\1', s)  # รร แล้วตามด้วยสระ เปลี่ยน รร เป็น ั น
    s = re.sub('รร', 'ัน', s)   #รร เฉยๆ เปลี่ยนเป็น ั น
    #print(s)

    if "ไ" in s or "ใ" in s : #ถ้าเป็นสระ ไ หรือ ใ ให้เปลี่ยนคําเป็นอัย
        s = "อัย"
    #print(s)

    if "ำ" in s: #ถ้าเป็นสระอําให้เปลี่ยนเป็นอัม
        s = "อัม"
    #print(s)

    s = re.sub("่", "", s) #ลบวรรณยุกต์
    s = re.sub("้", "", s)
    s = re.sub("๊", "", s)
    s = re.sub("๋", "", s)

    s = re.sub('จน์|มณ์|ณฑ์|ทร์|ตร์|[ก-ฮ]์|[ก-ฮ][ะ-ู]์', "", s) # 6.ลบการันต์
    #print(s)
    x = s


    s = re.sub('[ะ-์]', '', s) # 7. ตัดสระทั้งหมดที่เหลือ
    #print(s)
    y = s

    if len(s) >= 3 and (s[1] == "ร" or s[1] == "ล"):  #ลบตัวควบกลํ้า
        s = s.replace("ร", "")
        s = s.replace("ล", "")

    #print(s)

    first = set(x)
    second = set(y)
    d = list(first.symmetric_difference(second))#เอาค่าก่อนลบสระ กับหลังลบ สระมาลบกันเพื่อให้เหลือแต่สระ
    #print(d)


    sd = s[1:].translate(tu)#9 เอาsไปถอดรหัสเพื่อหามาตราตัวสะกด
    #print(sd)

    vw = ""
    for x in d:   #เอาdไปถอดรหัสเพื่อหาสระ
        wy = x.translate(tu2)
        vw = vw + wy

    #print(vw)

    return sd+vw

def oksound(w):
    cutword()
    z = rhyme(text)
    return z


cutword()
#print(data)
z = rhyme(text)
#print(z)
#convertdata()
#print(datas)
#find()
#print(i2)
#show()
#print(data0[:30])
