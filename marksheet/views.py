from django.shortcuts import render
from people.models import Student
from core.models import Batch
from .models import Marksheet, Scorecard
from notebooks.views import get_max_id_function

def all_current_terms(request):
    all_classes = Batch.objects.all().order_by('current_class')
    return render(request, 'marksheet/terms.html', {
        'classes' : all_classes
    })

def marksheet_view(request):
    if request.method == 'POST':
        data = request.POST
        this_batch = Batch.objects.filter(batch_id=data.get('batch')).first()

        # Create or get the marksheet
        marksheet_obj, created = Marksheet.objects.get_or_create(
            marksheet_id=str(get_max_id_function(Marksheet, 'marksheet_id') + 1),
            batch=this_batch,
            forclass=this_batch.current_class,
        )

        # Create scorecards for each student in the batch
        for student in Student.objects.filter(batch=this_batch):
            Scorecard.objects.get_or_create(
                student=student,
                marksheet_id=marksheet_obj,
                term=data.get('term', 1),
                defaults={
                    'hindi_theory': 0,
                    'hindi_assessment': 0,
                    'english_theory': 0,
                    'english_assessment': 0,
                    'maths_theory': 0,
                    'maths_assessment': 0,
                    'science_theory': 0,
                    'science_assessment': 0,
                    'sst_evs_theory': 0,
                    'sst_evs_assessment': 0,
                    'drawing_theory': 0,
                    'drawing_assessment': 0,
                    'computer_music_theory': 0,
                    'computer_music_assessment': 0,
                    'gk_theory': 0,
                    'gk_assessment': 0,
                    'punjabi_skt_theory': 0,
                    'punjabi_skt_assessment': 0,
                }
            )

    return render(request, 'marksheet/base_sheet.html', {
        'subjects': [
            'Hindi', 'English', 'Maths', 'Science',
            'Social Science', 'Punjabi', 'GK'
        ],
        'students': Student.objects.all(),
    })


def student_scorecard(request, student_id):
    return render(request, 'marksheet/student_sheet.html',{
        'subjects': ['Hindi', 'English', 'Maths', 'Science', 'Social Science', 'Punjabi', 'GK'],
        'scorecards' : [1,2,3]
    })