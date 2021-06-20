from django import forms


class TeacherForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254)
    room_number = forms.IntegerField()
    phone_number = forms.CharField(max_length=15)
    subjects = forms.CharField()


class UploadFileForm(forms.Form):
    file = forms.FileField()


class FilterForm(forms.Form):
    subjects = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
