""" views for marksheet app """
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
        return 'A++' + f"\t({score})"
    elif percentage >= 81:
        return 'A+' + f"\t({score})"
    elif percentage >= 71:
        return 'A' + f"\t({score})"
    elif percentage >= 61:
        return 'B' + f"\t({score})"
    elif percentage >= 51:
        return 'C' + f"\t({score})"
    elif percentage >= 41:
        return 'D' + f"\t({score})"
    elif percentage >= 33:
        return 'E' + f"\t({score})"
    else:
        return 'F' + f"\t({score})"

@login_required(login_url='/login')
@bronzelogger
def scorecard_pdf_download(request, student_id, sem):
    """
    Nothing
    """
    student = Student.objects.get(student_id=student_id)
    max_marks_per_subject = 100
    if student.batch.current_class < 6:
        max_marks_per_subject = 50
    scorecards = Scorecard.objects.filter(
        student=student).order_by('marksheet_id__term')
    i = 1
    final_marks = {
        'hindi_final_total': 0,
        'english_final_total': 0,
        'maths_final_total': 0,
        'science_final_total': 0,
        'sst_evs_final_total': 0,
        'drawing_final_total': 0,
        'computer_music_final_total': 0,
        'gk_final_total': 0,
        'punjabi_skt_final_total': 0,
        'hindi_final_percentage': 0,
        'english_final_percentage': 0,
        'maths_final_percentage': 0,
        'science_final_percentage': 0,
        'sst_evs_final_percentage': 0,
        'drawing_final_percentage': 0,
        'computer_music_final_percentage': 0,
        'gk_final_percentage': 0,
        'punjabi_skt_final_percentage': 0
    }
    for card in scorecards:
        card.hindi_total = card.hindi_theory + card.hindi_assessment
        card.english_total = card.english_theory + card.english_assessment
        card.maths_total = card.maths_theory + card.maths_assessment
        card.science_total = card.science_theory + card.science_assessment
        card.sst_evs_total = card.sst_evs_theory + card.sst_evs_assessment
        card.drawing_total = card.drawing_theory + card.drawing_assessment
        card.computer_music_total = card.computer_music_theory + card.computer_music_assessment
        card.gk_total = card.gk_theory + card.gk_assessment
        card.punjabi_skt_total = card.punjabi_skt_theory + card.punjabi_skt_assessment
        card.term_total = (
            card.hindi_total + card.english_total + card.maths_total +
            card.science_total + card.sst_evs_total + card.punjabi_skt_total
        )
        card.term_percentage = round((card.term_total / 500) * 100, 2)
        final_marks['hindi_final_total'] += card.hindi_total
        final_marks['hindi_final_percentage'] = round((final_marks['hindi_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['english_final_total'] += card.english_total
        final_marks['english_final_percentage'] = round((final_marks['english_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['maths_final_total'] += card.maths_total
        final_marks['maths_final_percentage'] = round((final_marks['maths_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['science_final_total'] += card.science_total
        final_marks['science_final_percentage'] = round((final_marks['science_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['sst_evs_final_total'] += card.sst_evs_total
        final_marks['sst_evs_final_percentage'] = round((final_marks['sst_evs_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['drawing_final_total'] += card.drawing_total
        final_marks['drawing_final_percentage'] = round((final_marks['drawing_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['computer_music_final_total'] += card.computer_music_total
        final_marks['computer_music_final_percentage'] = round((final_marks['computer_music_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['gk_final_total'] += card.gk_total
        final_marks['gk_final_percentage'] = round((final_marks['gk_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        final_marks['punjabi_skt_final_total'] += card.punjabi_skt_total
        final_marks['punjabi_skt_final_percentage'] = round((final_marks['punjabi_skt_final_total'] / (i * max_marks_per_subject)) * 100, 2)
        card.term_number = i
        i+=1
    
    # convert to grades
    final_marks['drawing_final_total'] = grade_this_score(final_marks['drawing_final_total'], max_marks_per_subject*3)
    final_marks['computer_music_final_total'] = grade_this_score(final_marks['computer_music_final_total'], max_marks_per_subject*3)
    final_marks['gk_final_total'] = grade_this_score(final_marks['gk_final_total'], max_marks_per_subject*3)
    for card in scorecards:
        card.drawing_total = grade_this_score(card.drawing_total, max_marks_per_subject)
        card.computer_music_total = grade_this_score(card.computer_music_total, max_marks_per_subject)
        card.gk_total = grade_this_score(card.gk_total, max_marks_per_subject)

    card_ids = [card.id for card in scorecards]
    sheet_template = 'scorecard_pdf/primary/'
    scorecard = []
    if student.batch.current_class > 8:
        sheet_template = 'scorecard_pdf/sen_sec/'
    elif student.batch.current_class > 5:
        sheet_template = 'scorecard_pdf/sec/'
    if sem < 4:
        scorecard = [card for card in scorecards if sem == card.term_number][0]
        sheet_template += 'sem_card.html'
    else:
        scorecard = scorecards[0]
        sheet_template += 'full_card.html'
    template = render_to_string(sheet_template, {
        'student': student,
        'scorecards': scorecards,
        'card_ids': card_ids,
        'card': scorecard,
    } | {**final_marks})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="scorecard_{student.student_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()

    # Student Result Section
    elements.append(Paragraph("Student Result", styles['Heading1']))
    elements.append(Spacer(1, 0.1*inch))

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

    # Term Data
    terms = [
        {
            'term': 'Term 1',
            'data': [
                ['Subject', 'Max Marks', '', 'Pass Marks', 'Obtained Marks', '', ''],
                ['', 'Theory', 'Assessment', '', 'Theory', 'Assessment', 'Total'],
                ['Hindi', '40', '10', '18', '40', '10', '50'],
                ['English', '40', '10', '18', '40', '10', '50'],
                ['Maths', '40', '10', '18', '40', '10', '50'],
                ['SST/EVS', '40', '10', '18', '40', '10', '50'],
                ['Drawing', '40', '10', '18', '40', '10', 'A++'],
                ['Computer/Music', '40', '10', '18', '0', '0', 'F'],
                ['GK', '40', '10', '18', '40', '10', 'A++'],
                ['Total', '', '', '', '', '', '200']
            ]
        },
        {
            'term': 'Term 2',
            'data': [
                ['Subject', 'Max Marks', '', 'Pass Marks', 'Obtained Marks', '', ''],
                ['', 'Theory', 'Assessment', '', 'Theory', 'Assessment', 'Total'],
                ['Hindi', '40', '10', '18', '40', '10', '50'],
                ['English', '40', '10', '18', '40', '0', '40'],
                ['Maths', '40', '10', '18', '0', '0', '0'],
                ['SST/EVS', '40', '10', '18', '0', '0', '0'],
                ['Drawing', '40', '10', '18', '0', '0', 'F'],
                ['Computer/Music', '40', '10', '18', '0', '0', 'F'],
                ['GK', '40', '10', '18', '0', '0', 'F'],
                ['Total', '', '', '', '', '', '90']
            ]
        },
        {
            'term': 'Term 3',
            'data': [
                ['Subject', 'Max Marks', '', 'Pass Marks', 'Obtained Marks', '', ''],
                ['', 'Theory', 'Assessment', '', 'Theory', 'Assessment', 'Total'],
                ['Hindi', '40', '10', '18', '0', '0', '0'],
                ['English', '40', '10', '18', '0', '0', '0'],
                ['Maths', '40', '10', '18', '0', '0', '0'],
                ['SST/EVS', '40', '10', '18', '0', '0', '0'],
                ['Drawing', '40', '10', '18', '0', '0', 'F'],
                ['Computer/Music', '40', '10', '18', '0', '0', 'F'],
                ['GK', '40', '10', '18', '0', '0', 'F'],
                ['Total', '', '', '', '', '', '0']
            ]
        }
    ]

    # Add terms to elements
    for term in terms:
        elements.append(Paragraph(term['term'], styles['Heading2']))
        t = Table(term['data'], colWidths=[1.5*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch])
        t.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('SPAN', (1, 0), (2, 0)),  # Max Marks
            ('SPAN', (4, 0), (6, 0)),  # Obtained Marks
            ('SPAN', (0, -1), (5, -1)),  # Total label span
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

    # Overall Summary
    overall_summary = [
        ['Subject', 'Obtained Marks', '', '', 'Total', 'Percentage'],
        ['', 'Term 1', 'Term 2', 'Term 3', '', ''],
        ['Hindi', '50', '50', '0', '100', '66.67'],
        ['English', '50', '40', '0', '90', '60.0'],
        ['Maths', '50', '0', '0', '50', '33.33'],
        ['Drawing', 'A++', 'F', 'F', 'A++', '33.33'],
        ['Computer/Music', 'F', 'F', 'F', 'F', '0.0'],
        ['GK', 'A++', 'F', 'F', 'A++', '33.33']
    ]

    elements.append(Paragraph("Overall Summary", styles['Heading2']))
    t_summary = Table(overall_summary, colWidths=[1.5*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch, 0.75*inch])
    t_summary.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('SPAN', (1, 0), (3, 0)),  # Obtained Marks
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
    elements.append(t_summary)

    doc.build(elements)
    return response