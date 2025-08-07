from django.shortcuts import render
from people.models import Student

def marksheet_view(request):
    return render(request, 'marksheet/base_sheet.html', {
        'subjects': ['Hindi', 'English', 'Maths', 'Science', 'Social Science', 'Punjabi', 'GK'],
        'students': Student.objects.all(),
    })