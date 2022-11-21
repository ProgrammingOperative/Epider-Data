from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from fastai.vision.all import *
import pathlib
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .models import Report
from django.contrib.auth.models import User

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


path = Path()
learn_inf = load_learner(path/"models/version1.pkl")

user = User.objects.filter(username="waCira").first()

def home(request):
    context = {'a': "Hellow Javis"}
    return render(request, 'skin_classifier/home.html', context)


def classify(request):
    fileobj = request.FILES['filepath']
    fs = FileSystemStorage()
    fs.save(fileobj.name, fileobj)
    filepathname = fs.url(fileobj)
    print(fileobj)
    pt = f"{path.cwd()}/MEDIA/{fileobj}"
    print(filepathname)
    img = PILImage.create(pt)
    pred, pred_idx, probs = learn_inf.predict(img)
    prob = float(f"{probs[pred_idx]:.04f}")

    stat = ""
    if pred == 'malignant':
        if prob > 0.9999:
            stat = "VERY URGENT!!!"
            messages.warning(request, f"VERY URGENT!!!")
        elif prob > 0.8000:
            stat = "URGENT!!!"
            messages.warning(request, f"URGENT!!!")
        else:
            stat = "CHECK!!"
            messages.info(request, f"CHECK!!")

    elif pred == 'benign':
        if prob > 0.9999:
            stat = 'SKIN OKAY'
            messages.success(request, f"SKIN OKAY")
        elif prob > 0.8000 :
            stat = 'CAN WAIT'
            messages.success(request, f"CAN WAIT")
        else:
            stat = 'ROOM FOR CHECK'
            messages.info(request, f'ROOM FOR CHECK')
    else:
        stat = "Uknown"

    dt = Report(sample_id = fileobj, prediction= pred, probability=prob, urgency=stat, organization=user)
    dt.save()

    context = {'filepathname': filepathname, "filename":fileobj, "pred":pred, 
                "pred_idx": pred_idx, "probs":f"{probs[pred_idx]:.04f}", 'stat': stat }
    
    return render(request, 'skin_classifier/classify.html', context)


def pdf_report(request):
    #Create bytestream buffer
    buf = io.BytesIO()

    #Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    report_data = Report.objects.all()
    #Add some line of text
    lines = []
    for r_data in report_data:
        lines.append(f"===================== {str(r_data.organization)} Sample Results ====================")
        lines.append("")
        lines.append(f"LEVEL OF URGENCY: {r_data.urgency}")
        lines.append(f"DATE OF DIAGNOSIS: {str(r_data.date)}")
        lines.append(f"SAMPLE ID : {r_data.sample_id}")
        lines.append(f"SKIN CONDITION CLASSIFICATION: {r_data.prediction}")
        lines.append(f"DETERMINING PROBABILITY: {str(r_data.probability)}")
        lines.append("=======================================================================================")
        lines.append("")

        
    for line in lines:
        textob.textLine(line)
    
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='report.pdf')