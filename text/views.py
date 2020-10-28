from django.shortcuts import render
from django.http import HttpResponse
from .forms import DocumentForm, TextInputForm
from django.views.generic import View, TemplateView

# import request
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from bs4 import BeautifulSoup as bs

from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io

import cv2
import pytesseract
from pathlib import Path
import os
import numpy as np

# Create your views here.


def index(request):
    my_dict = {'insert_me': "Hello, Welcome To My official Website"}
    return render(request, 'text/index.html', context=my_dict)

class LoginView(TemplateView):
    template_name = 'text/login.html'
# def login(request):
#     return render(request, 'text/login.html')
class AboutView(TemplateView):
    template_name = 'text/about.html'

class MediaView(TemplateView):
    template_name = 'text/media.html'

class AudioView(TemplateView):
    template_name = 'text/audio.html'

# function to extract text data only from input
def get_only_text(text_pasted):
    clean_text = bs(text_pasted, features="html.parser").get_text()
    return clean_text

def textlize(request):
    result = ''
    form = TextInputForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            raw_text = form.cleaned_data["text_in"]
            cleaned_text = get_only_text(raw_text)
            selected = form.cleaned_data.get('slize_size')
            if selected:
                size_dict = {"slize_pointfive":0.005, "slize_one":0.01, "slize_five":0.05,
                            "slize_ten":0.10, "slize_twenty":0.20, "slize_thirty":0.30,
                            "slize_forty":0.40, "slize_fifty":0.50}
                for k,v in size_dict.items():
                    if selected == k:
                        result = summarize(cleaned_text, ratio=v)
                        return render(request, 'text/textlize.html', {'form':form, 'result':result})
            else:
                result = summarize(cleaned_text, ratio=0.25)
                return render(request, 'text/textlize.html', {'form':form, 'result':result})
    else:
        form = TextInputForm()
    return render(request, 'text/textlize.html', {'form':form})





def extract_information(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    # with open(pdf_path, 'rb') as fh:
    for page in PDFPage.get_pages(pdf_path,
                                  caching=True,
                                  check_extractable=True):
        page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    return (text)


class ConvertFile(View):
    template_name = 'text/convertfile.html'
    form_1 = TextInputForm
    form_2 = DocumentForm
    def get(self, request):
        form1 = self.form_1(None)
        form2 = self.form_2(None)
        return render(request, self.template_name, {'form1':form1, 'form2':form2})
    def post(self, request):
        result = ''
        form1 = self.form_1(None)
        form2 = self.form_2(None)
        if (request.method == 'POST' and 'convertbutton' in request.POST):
            form2 = DocumentForm(request.POST, request.FILES)
            if form2.is_valid():
                file_upload = form2.cleaned_data["file_in"]
                file_name = request.FILES['file_in'].name
                if not file_name.endswith('.pdf'):
                    img = cv2.imdecode(np.fromstring(request.FILES['file_in'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
                    file_extract = pytesseract.image_to_string(img, config=r'-l eng --oem 3 --psm 6')
                    return render(request, self.template_name, {'form1':form1, 'form2':form2, 'file_extract':file_extract})
                else:
                    file_extract = extract_information(file_upload)
                    return render(request, self.template_name, {'form1':form1, 'form2':form2, 'file_extract':file_extract})
        if (request.method == 'POST' and 'summarizebutton' in request.POST):
            form1 = TextInputForm(request.POST)
            if form1.is_valid():
                raw_text = form1.cleaned_data["text_in"]
                cleaned_text = get_only_text(raw_text)
                selected = form1.cleaned_data.get('slize_size')
                if selected:
                    size_dict = {"slize_pointfive":0.005, "slize_one":0.01, "slize_five":0.05,
                                "slize_ten":0.10, "slize_twenty":0.20, "slize_thirty":0.30,
                                "slize_forty":0.40, "slize_fifty":0.50}
                    for k,v in size_dict.items():
                        if selected == k:
                            result = summarize(cleaned_text, ratio=v)
                            return render(request, self.template_name, {'form1':form1, 'form2':form2,'result':result})
                else:
                    result = summarize(cleaned_text, ratio=0.25)
                    return render(request, self.template_name, {'form1':form1, 'form2':form2, 'result':result})
        else:
            return render(request, self.template_name, {'form1':form1, 'form2':form2})
