from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from fastai.vision.all import *


path = Path()
learn_inf = load_learner(path/"models/version1.pkl")


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

    context = {'filepathname': filepathname, "filename":fileobj, "pred":pred, "pred_idx": pred_idx, "probs":probs[pred_idx].data}
    return render(request, 'skin_classifier/classify.html', context)

# Create your views here.
