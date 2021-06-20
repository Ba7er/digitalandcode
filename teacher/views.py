from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render
from django.urls import reverse

from .forms import TeacherForm, UploadFileForm, FilterForm
from .models import Teacher
from subject.models import Subject
from .utils import handle_uploaded_file

from django.http import HttpResponse
from django.contrib import messages


# Create your views here.


def index(request):
    res = request.GET.get('id')
    teachers_list = Teacher.objects.filter(last_name__startswith='')
    create_teacher_form = TeacherForm()
    uploadFileForm = UploadFileForm()
    filterForm = FilterForm()
    return render(request, 'teacher/index.html', {'teachers_list': teachers_list, 'create_teacher_form': create_teacher_form, 'uploadFileForm': uploadFileForm, 'filterForm': filterForm})


def profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    form = TeacherForm(request.POST)
    subjects = teacher.subjects.all()
    return render(request, 'teacher/profile.html', {'teacher': teacher, 'subjects': subjects, 'form': form})


def filter(request):
    create_teacher_form = TeacherForm()
    uploadFileForm = UploadFileForm()
    if request.method == 'POST':
        filterForm = FilterForm(request.POST)
        if filterForm.is_valid():
            teachers_list = Teacher.objects.filter(
                last_name__startswith=filterForm.cleaned_data['last_name']).filter(subjects__subject=filterForm.cleaned_data["subjects"])
            return render(request, 'teacher/index.html', {'teachers_list': teachers_list, 'create_teacher_form': create_teacher_form, 'uploadFileForm': uploadFileForm, 'filterForm': filterForm})

    else:
        return HttpResponse('none')


def create_bulk(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            # check if myfile.name is needed
            filename = fs.save(myfile.name, myfile)
            teachers_list = handle_uploaded_file(filename)
            for teacher in teachers_list:
                try:
                    new_teacher = Teacher(first_name=teacher["first_name"],
                                          last_name=teacher["last_name"], email=teacher["email"], phone_number=teacher["phone_number"], room_number=teacher["room_number"])
                    new_teacher.save()
                    for subject in teacher["subjects"]:
                        subject = Subject(subject=subject)
                        subject.save()
                        new_teacher.subjects.add(subject)
                except ValidationError as e:
                    print('error is', e)

    print(teachers_list)

    return HttpResponseRedirect(reverse('teacher:index'))


def create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            # A model form can be used instead.
            subject = (Subject(subject=form.cleaned_data['subjects']))
            subject.save()
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            room_number = form.cleaned_data['room_number']
            new_teacher = Teacher(first_name=first_name,
                                  last_name=last_name, email=email, phone_number=phone_number, room_number=room_number)
            new_teacher.save()
            new_teacher.subjects.add(subject)

            return HttpResponseRedirect(reverse('teacher:index'))
        else:
            return HttpResponseRedirect(reverse('teacher:index'))

    else:
        return HttpResponseRedirect(reverse('teacher:index'))
