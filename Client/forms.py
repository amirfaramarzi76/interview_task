from django import forms

class JSONFileUploadForm(forms.Form):
    json_file = forms.FileField(label='Upload JSON File', help_text='Select a JSON file to send to the server.')
