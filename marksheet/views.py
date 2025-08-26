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

def marksheet_view(request, sheet_id):
    data = {}
    if request.method == 'POST':
        data = request.POST

    # if its a marksheet made from the terms page
    # It has batch and term value, which will be used to find marksheet
    if sheet_id == "new":
        this_batch = Batch.objects.filter(batch_id=data.get('batch')).first()
        term_value = f"2025-26_{data.get('term')}"
        marksheet_obj, created_mks = Marksheet.objects.get_or_create(
                batch=this_batch,
                term=term_value,
                defaults={
                    'marksheet_id': "marksheet_" + str(get_max_id_function(Marksheet, 'marksheet_id') + 1),
                    'batch':this_batch,
                    'term':term_value,
                    'forclass': this_batch.current_class,
                }
        )
    else:
        # it its an updating marksheet
        # existing marksheet object will be used 
        marksheet_obj = Marksheet.objects.get(
                marksheet_id=sheet_id
        )
        this_batch = marksheet_obj.batch
        term_value = marksheet_obj.term
             
    # --- if new existing markshit; createscorecard for all ---
    for student in Student.objects.filter(batch=this_batch):
            scorecard_obj, created_sc = Scorecard.objects.get_or_create(
                student=student,
                marksheet_id=marksheet_obj,
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

            # --- If existing scorecard, update marks from data ---
            if not created_sc:
                scorecard_obj.hindi_theory = data.get(f"hindi_theory_{student.student_id}", scorecard_obj.hindi_theory)
                scorecard_obj.hindi_assessment = data.get(f"hindi_assessment_{student.student_id}", scorecard_obj.hindi_assessment)
                scorecard_obj.english_theory = data.get(f"english_theory_{student.student_id}", scorecard_obj.english_theory)
                scorecard_obj.english_assessment = data.get(f"english_assessment_{student.student_id}", scorecard_obj.english_assessment)
                scorecard_obj.maths_theory = data.get(f"maths_theory_{student.student_id}", scorecard_obj.maths_theory)
                scorecard_obj.maths_assessment = data.get(f"maths_assessment_{student.student_id}", scorecard_obj.maths_assessment)
                scorecard_obj.science_theory = data.get(f"science_theory_{student.student_id}", scorecard_obj.science_theory)
                scorecard_obj.science_assessment = data.get(f"science_assessment_{student.student_id}", scorecard_obj.science_assessment)
                scorecard_obj.sst_evs_theory = data.get(f"sst_evs_theory_{student.student_id}", scorecard_obj.sst_evs_theory)
                scorecard_obj.sst_evs_assessment = data.get(f"sst_evs_assessment_{student.student_id}", scorecard_obj.sst_evs_assessment)
                scorecard_obj.drawing_theory = data.get(f"drawing_theory_{student.student_id}", scorecard_obj.drawing_theory)
                scorecard_obj.drawing_assessment = data.get(f"drawing_assessment_{student.student_id}", scorecard_obj.drawing_assessment)
                scorecard_obj.computer_music_theory = data.get(f"computer_music_theory_{student.student_id}", scorecard_obj.computer_music_theory)
                scorecard_obj.computer_music_assessment = data.get(f"computer_music_assessment_{student.student_id}", scorecard_obj.computer_music_assessment)
                scorecard_obj.gk_theory = data.get(f"gk_theory_{student.student_id}", scorecard_obj.gk_theory)
                scorecard_obj.gk_assessment = data.get(f"gk_assessment_{student.student_id}", scorecard_obj.gk_assessment)
                scorecard_obj.punjabi_skt_theory = data.get(f"punjabi_skt_theory_{student.student_id}", scorecard_obj.punjabi_skt_theory)
                scorecard_obj.punjabi_skt_assessment = data.get(f"punjabi_skt_assessment_{student.student_id}", scorecard_obj.punjabi_skt_assessment)
                scorecard_obj.save()

    scorecards = Scorecard.objects.filter(
            marksheet_id=marksheet_obj
        ).order_by('student__roll_number')
    
    sheet_template = 'marksheet_templates/marksheet_primary.html'
    if marksheet_obj.forclass > 8:
        sheet_template = 'marksheet_templates/marksheet_senior_sec.html'
    elif marksheet_obj.forclass > 5:
        sheet_template = 'marksheet_templates/marksheet_sec.html'

    return render(request, sheet_template, {
        'subjects': [
            'Hindi', 'English', 'Maths', 'Science',
            'Social Science', 'Punjabi', 'GK'
        ],
        'scorecards': scorecards,
        'marksheet': marksheet_obj
    })



def student_scorecard(request, student_id):
    student = Student.objects.get(student_id=student_id)
    marksheets = Marksheet.objects.filter(batch=student.batch,forclass=student.batch.current_class).order_by('term')
    scorecards = Scorecard.objects.filter(student=student,marksheet_id__in=marksheets).order_by('marksheet_id__term')
    i = 1
    for card in scorecards:
        card.term_number = i
        i += 1
    card_ids = [card.id for card in scorecards]
    return render(request, 'marksheet/student_scorecard.html',{
        'subjects': ['Hindi', 'English', 'Maths', 'Science', 'SST/ EVS', 'drawing', 'computer', 'gk', 'punjabi'],
        'student':student,
        'scorecards':scorecards,
        'card_ids':card_ids
    })