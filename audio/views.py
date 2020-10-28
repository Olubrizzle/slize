from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from .forms import AudioForm, TextInputForm

import speech_recognition as sr

import sys


# Create your views here.

class IndexView(TemplateView):
    template_name = 'audio/index.html'



class UploadView(View):
    template_name = 'audio/uploadaudio.html'
    form_1 = TextInputForm
    form_2 = AudioForm
    def get(self, request):
        form1 = self.form_1(None)
        form2 = self.form_2(None)
        return render(request, self.template_name, {'form1':form1, 'form2':form2})
    def post(self, request):
        result = ''
        form1 = self.form_1(None)
        form2 = self.form_2(None)
        if (request.method == 'POST' and 'convertbutton' in request.POST):
            form2 = AudioForm(request.POST, request.FILES)
            if form2.is_valid():
                file_upload = form2.cleaned_data["file_in"]
                r = sr.Recognizer()
                with sr.AudioFile(file_upload) as source:
                    r.adjust_for_ambient_noise(source, duration=5)
                    audio_data = r.record(source)
                    try:
                        audio_extract = r.recognize_google(audio_data)
                        print(audio_extract)
                        # audio_extract = r.recognize_sphinx(audio_data)
                        return render(request, self.template_name, {'form1':form1, 'form2':form2, 'audio_extract':audio_extract})
                    except sr.UnknownValueError:
                        return render(request, self.template_name, {'form1':form1, 'form2':form2})
                    except sr.RequestValueError:
                    # except sr.RequestValueError as e:
                        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
                        return render(request, self.template_name, {'form1':form1, 'form2':form2})
        else:
            return render(request, self.template_name, {'form1':form1, 'form2':form2})


class RecordView(View):
    template_name = 'audio/recordaudio.html'
