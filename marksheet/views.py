""" views for marksheet app """
from collections import defaultdict
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from notebooks.views import get_max_id_function
from people.models import Student
from core.models import Batch
from .models import Marksheet, Scorecard
from django.contrib.auth.decorators import login_required
from utils.bronzelogger import bronzelogger
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

@login_required(login_url='/login')
@bronzelogger
def all_current_terms(request):
    """
    returns list of all current classes
    """
    all_classes = Batch.objects.all().order_by('current_class')
    return render(request, 'marksheet/terms.html', {
        'classes' : all_classes
    })

@login_required(login_url='/login')
@bronzelogger
def marksheet_view(request, sheet_id):
    """
    view or create marksheet
    """
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
                    'marksheet_id': "marksheet_" + str(get_max_id_function(
                        Marksheet, 'marksheet_id') + 1),
                    'batch':this_batch,
                    'term':term_value,
                    'forclass': this_batch.current_class,
                }
        )
        if not created_mks:
            # if marksheet already exists, redirect to that marksheet
            sheet_id = marksheet_obj.id
            return marksheet_view(request, sheet_id)
    else:
        # it its an updating marksheet
        # existing marksheet object will be used
        marksheet_obj = Marksheet.objects.get(
                id=sheet_id
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
                    'punjabi_skt_assessment': 0        
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



@login_required(login_url='/login')
@bronzelogger
def student_scorecard(request, student_id):
    """
    returns students marks scarcards in details
    """
    student = Student.objects.get(student_id=student_id)
    marksheets = Marksheet.objects.filter(
        batch=student.batch,
        forclass=student.batch.current_class).order_by('term')
    scorecards = Scorecard.objects.filter(
        student=student,
        marksheet_id__in=marksheets).order_by('marksheet_id__term')
    i = 1
    for card in scorecards:
        card.term_number = i
        i += 1
    card_ids = [card.id for card in scorecards]
    sheet_template = 'scorecard_templates/scorecard_primary.html'
    if marksheets[0].forclass > 8:
        sheet_template = 'scorecard_templates/scorecard_senior_sec.html'
    elif marksheets[0].forclass > 5:
        sheet_template = 'scorecard_templates/scorecard_sec.html'
    return render(request, sheet_template ,{
        'student':student,
        'scorecards':scorecards,
        'card_ids':card_ids,
        'card':scorecards[0]
    })

@login_required(login_url='/login')
def link_callback(uri, rel):
    """
    Convert HTML URIs from {% static %} or MEDIA_URL to absolute system paths
    so xhtml2pdf can access them.
    """
    from django.conf import settings
    from django.contrib.staticfiles import finders
    import os

    if uri.startswith(settings.STATIC_URL):
        path = uri.replace(settings.STATIC_URL, '')
        absolute_path = finders.find(path)
        if absolute_path:
            if isinstance(absolute_path, (list, tuple)):
                absolute_path = absolute_path[0]
            return absolute_path

    if settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
        path = uri.replace(settings.MEDIA_URL, '')
        return os.path.join(settings.MEDIA_ROOT, path)

    return uri  # leave absolute URLs as-is

def grade_this_score(score, max_score):
    """
    Convert score to grade
    """
    percentage = (score / max_score) * 100
    if percentage >= 91:
        return 'A++' + f"({score})"
    elif percentage >= 81:
        return 'A+' + f"({score})"
    elif percentage >= 71:
        return 'A' + f"({score})"
    elif percentage >= 61:
        return 'B' + f"({score})"
    elif percentage >= 51:
        return 'C' + f"({score})"
    elif percentage >= 41:
        return 'D' + f"({score})"
    elif percentage >= 33:
        return 'E' + f"({score})"
    else:
        return 'F' + f"({score})"

@login_required(login_url='/login')
@bronzelogger
def scorecard_pdf_download(request, student_id, sem):
    student = Student.objects.get(student_id=student_id)
    class_level = student.batch.current_class
    max_marks_per_subject = 100 if class_level >= 6 else 50
    theory_max = 80 if class_level >= 6 else 40
    assess_max = 20 if class_level >= 6 else 10
    pass_marks = 35 if class_level >= 6 else 18

    scorecards = Scorecard.objects.filter(student=student).order_by('marksheet_id__term')

    subject_list = [
        {'name': 'Hindi', 'key': 'hindi', 'graded': False},
        {'name': 'English', 'key': 'english', 'graded': False},
        {'name': 'Maths', 'key': 'maths', 'graded': False},
        {'name': 'Science', 'key': 'science', 'graded': False},
        {'name': 'SST/EVS', 'key': 'sst_evs', 'graded': False},
        {'name': 'Punjabi/Skt', 'key': 'punjabi_skt', 'graded': False},
        {'name': 'Drawing', 'key': 'drawing', 'graded': True},
        {'name': 'Computer/Music', 'key': 'computer_music', 'graded': True},
        {'name': 'GK', 'key': 'gk', 'graded': True},
    ]

    if class_level <= 5:
        show_keys = ['hindi', 'english', 'maths', 'sst_evs', 'drawing', 'computer_music', 'gk']
    elif 6 <= class_level <= 8:
        show_keys = ['hindi', 'english', 'maths', 'science', 'sst_evs', 'punjabi_skt', 'computer_music', 'gk']
    else:
        show_keys = ['hindi', 'english', 'maths', 'science', 'sst_evs']

    main_keys = [s['key'] for s in subject_list if s['key'] in show_keys and not s['graded']]
    graded_keys = [s['key'] for s in subject_list if s['key'] in show_keys and s['graded']]
    num_main_subjects = len(main_keys)

    final_marks = {f'{key}_final_total': 0 for key in show_keys}
    final_marks.update({f'{key}_final_percentage': 0 for key in show_keys})
    completed_counts = defaultdict(int)

    for index, card in enumerate(scorecards):
        card.term_number = index + 1
        for sub in subject_list:
            key = sub['key']
            theory = getattr(card, f'{key}_theory', 0)
            assessment = getattr(card, f'{key}_assessment', 0)
            total = theory + assessment
            setattr(card, f'{key}_total', total)
            if key in show_keys:
                final_marks[f'{key}_final_total'] += total
                if total > 0 and key in graded_keys:
                    completed_counts[key] += 1

        card.term_total = sum(getattr(card, f'{key}_total') for key in main_keys)
        max_term_total = num_main_subjects * max_marks_per_subject
        card.term_percentage = round((card.term_total / max_term_total * 100) if max_term_total > 0 else 0, 2)

        for key in graded_keys:
            score = getattr(card, f'{key}_total')
            setattr(card, f'{key}_total', grade_this_score(score, max_marks_per_subject))

    num_terms = len(scorecards)
    for key in show_keys:
        total_sum = final_marks[f'{key}_final_total']
        final_marks[f'{key}_final_percentage'] = round((total_sum / (num_terms * max_marks_per_subject)) * 100, 2) if num_terms > 0 else 0

    for key in graded_keys:
        num_completed = completed_counts[key]
        if num_completed > 0:
            avg_score = final_marks[f'{key}_final_total'] / num_completed
            final_grade = grade_this_score(avg_score, max_marks_per_subject)
        else:
            final_grade = 'F'
        final_marks[f'{key}_final_total'] = final_grade

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="scorecard_{student.student_id}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Student Result", styles['Heading1']))
    elements.append(Spacer(1, 0.1*inch))

    card = next((card for card in scorecards if card.term_number == sem), scorecards[0]) if sem < 4 else scorecards[0] if scorecards else None
    if card:
        data_student = [
            ['Student Name', student.name],
            ['Class', card.marksheet_id.forclass],
            ['Roll Number', student.roll_number],
        ]
        t_student = Table(data_student, colWidths=[2*inch, 2*inch])
        t_student.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(t_student)
        elements.append(Spacer(1, 0.2*inch))

    selected_cards = [card] if sem < 4 else scorecards
    terms = []
    for card in selected_cards:
        term_data = [
            ['Subject', 'Max Marks', '', 'Pass Marks', 'Obtained Marks', '', ''],
            ['', 'Theory', 'Assessment', '', 'Theory', 'Assessment', 'Total'],
        ]
        for sub in [s for s in subject_list if s['key'] in show_keys]:
            key = sub['key']
            th = getattr(card, f'{key}_theory', 0)
            ass = getattr(card, f'{key}_assessment', 0)
            tot = getattr(card, f'{key}_total')
            term_data.append([sub['name'], str(theory_max), str(assess_max), str(pass_marks), str(th), str(ass), str(tot)])
        term_data.append(['Total', '', '', '', '', '', str(card.term_total)])
        terms.append({'term': f'Term {card.term_number}', 'data': term_data})

    for term in terms:
        elements.append(Paragraph(term['term'], styles['Heading2']))
        t = Table(term['data'], colWidths=[1.5*inch, 0.75*inch, 0.9*inch, 0.75*inch, 0.75*inch, 0.9*inch, 0.75*inch])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('SPAN', (1, 0), (2, 0)),
            ('SPAN', (4, 0), (6, 0)),
            ('SPAN', (0, -1), (5, -1)),
            ('ALIGN', (0, -1), (5, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 0.2*inch))

    if sem >= 4:
        num_terms = len(scorecards)
        overall_summary = [
            ['Subject', 'Obtained Marks', '', '', 'Total', 'Percentage'],
            [''] + [ 'term ' + str(i) for i in range(1,4)] + ['', ''],
        ]
        for sub in [s for s in subject_list if s['key'] in show_keys]:
            key = sub['key']
            term_totals = [str(getattr(c, f'{key}_total')) for c in scorecards]
            tot = final_marks[f'{key}_final_total']
            perc = final_marks[f'{key}_final_percentage']
            overall_summary.append([sub['name']] + term_totals + [str(tot), str(perc)])

        col_widths = [1.5*inch] + [0.75*inch] * num_terms + [0.75*inch, 0.75*inch]
        t_summary = Table(overall_summary, colWidths=col_widths)
        t_summary.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('SPAN', (1, 0), (1 + num_terms - 1, 0)),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        elements.append(Paragraph("Overall Summary", styles['Heading2']))
        elements.append(t_summary)

    doc.build(elements)
    return response