import speech_recognition as sr
import spacy
import math
from flask import Flask, render_template,jsonify,request
nlp = spacy.load('en')
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# from datetime import date
import subprocess
from flask_mail import Mail,Message


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Speak Now')
        audio = recognizer.listen(source)
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable/unresponsive"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"
    return response

#################
app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#personalinfo
@app.route('/personalinfo',methods=['POST'])
def detect_pi():
    print('detecting voice')
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    response = recognize_speech_from_mic(recognizer, mic)
    print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n{}\n' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription']))
   
    if(response['transcription'] != None):
        data1 = nlp(response['transcription'])
        keywords = []
        for word in data1.ents:
            print(word.text,word.label_)
            keywords.append(word.text)
        print(keywords)
        data1_split = data1.text.split()
        print(data1_split)
        name = keywords[0] if(keywords!=[]) else "Null"
        age = ""
        gender = ""
        for i in range(len(data1_split)):
            if(data1_split[i]=='age'):
                if(data1_split[i+1] != 'is'):
                    age = "" if(math.isnan(int(data1_split[i+1]))) else data1_split[i+1]
                else:
                    age = "" if(math.isnan(int(data1_split[i+2]))) else data1_split[i+2]
            if(data1_split[i]=='gender'):
                if(data1_split[i+1] != 'is'):
                    gender = data1_split[i+1]
                else:
                    gender = data1_split[i+1]
        if(age == ""):
            age = "Null"
        if(gender == ""):
            gender = "Null"
    else:
        name = "Null"
        age = "Null"
        gender = "Null"
    print("Name - ",name,"Age - ",age,"Gender - ",gender)
    return jsonify({"name": name, "age": age, "gender":gender})

#symptoms
@app.route('/symptoms',methods=['POST'])
def detect_symptoms():
    print('detecting voice')
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    response = recognize_speech_from_mic(recognizer, mic)
    print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n{}\n' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription']))
    if(response['transcription'] != None):
        symptoms = response['transcription']
        print(symptoms)
    else:
        symptoms='Null'
    symptoms_split=symptoms.lower()
    symptoms_split = symptoms.split(' next ')
    print(symptoms_split)
    return jsonify({"symptoms": symptoms_split})

#diagnosis
@app.route('/diagnosis',methods=['POST'])
def detect_diagnosis():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    response = recognize_speech_from_mic(recognizer, mic)
    print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n{}\n' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription']))
       
    if(response['transcription'] != None):
        diagnosis = response['transcription']
        print(diagnosis)
    else:
        diagnosis = "Null"
    return jsonify({"diagnosis": diagnosis})

#prescription
@app.route('/prescription',methods=['POST'])
def prescription():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    response = recognize_speech_from_mic(recognizer, mic)
    print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n{}\n' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription']))
   
    if(response['transcription'] != None):
        prescrip = response['transcription']
    else:
        prescrip = "Null"
    prescrip=prescrip.lower()
    prescrip_split = prescrip.split(' next ')
    print(prescrip_split)
    return jsonify({"prescription": prescrip_split})

#commetns
@app.route('/comments',methods=['POST'])
def comments():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    response = recognize_speech_from_mic(recognizer, mic)
    print('\nSuccess : {}\nError   : {}\n\nText from Speech\n{}\n{}\n' \
          .format(response['success'],
                  response['error'],
                  '-'*17,
                  response['transcription']))
       
    if(response['transcription'] != None):
        comments = response['transcription']
        print(comments)
    else:
        comments = "Null"
    return jsonify({"comments": comments})

##FINAL##
@app.route('/createpdf',methods=['POST'])
def createpdf():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    symptoms = request.form['symptoms']
    diagnosis = request.form['diagnosis']
    prescription = request.form['prescription']
    comments = request.form['comments']
    # today = date.today()

    pdf = canvas.Canvas(name+" Prescription.pdf", pagesize=letter)
    pdf.setTitle("Prescription")
    pdf.setLineWidth(.3)
    pdf.setFont('Helvetica-Bold',32)
    pdf.drawCentredString(300,750,'KEM Hospital')
    pdf.line(20,740,590,740)

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(440,720,'DATE:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(500,720,'22/11/2020')

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,720,'Dr. Shivangini Arora')
    pdf.setFont('Helvetica', 10)
    pdf.drawString(30,708,"M.B.B.S.")

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,683,'Patient Name:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(135,683,name)

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,663,'Age:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(70,663,age)

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(120,663,'Gender:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(183,663,gender)

    pdf.line(20,650,590,650)

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,620,'Symptoms:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(117,620,symptoms)

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,590,'Diagnosis:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(114,590,diagnosis)

    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,560,'Prescription:')
    pdf.setFont('Helvetica', 15)
    prescrip_split = prescription.split(',')
    for i in range(len(prescrip_split)):
        x = 560 - 20*i
        pdf.drawString(130,x,prescrip_split[i])
    x = x - 30
    pdf.setFont('Helvetica-Bold', 15)
    pdf.drawString(30,x,'Other Comments:')
    pdf.setFont('Helvetica', 15)
    pdf.drawString(166,x,comments)

    pdf.save()
    subprocess.Popen([name+' Prescription.pdf'],shell=True)
    return jsonify({'success': 'yes'})


if __name__== '__main__':
    app.run(debug=True)

