from django.db import models
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core import serializers
from .models import Student, NotebookSubmission, SubmissionRecord, Subject, Teacher, Batch
import json
import time

print_arg = "\n sys: "
def get_max_id_function(class_name:models.Model, id_name:str):
    max_list = [int(vals[id_name].split('_')[-1]) for vals in class_name.objects.values(id_name)]
    return max(max_list) if max_list else 0

def list_checks(request):        
    batches = Batch.objects.all().order_by('current_class')
    subjects = Subject.objects.all()
    return render(request, 'nb_checks/list_checks.html', {
        'records' :SubmissionRecord.objects.all(),
        'batches' :batches,
        'batches_json':json.loads(serializers.serialize('json', batches)),
        'subjects':Subject.objects.all(),
        'subjects_json':json.loads(serializers.serialize('json', subjects)),
        'teachers':Teacher.objects.all()
    })

def nb_checking(request, check_id):
    if request.method == "POST":    
        # get an existing or create a record
        data = request.POST
        associated_teacher = Teacher.objects.filter(teacher_id = data.get('associated_teacher')).first()
        associated_subject = Subject.objects.filter(      code = data.get('associated_subject')).first()
        associated_batch   = Batch.objects.filter(    batch_id = data.get('associated_batch')  ).first()

        if data.get('new-check',0) == 'add-new-check-record':
            temp_records = [{'student':student} for student in Student.objects.filter(batch=associated_batch).order_by('roll_number') ]
            return render(request, 'nb_checks/nb_checking.html', {
                        'check_id':check_id,
                        'teacher' :associated_teacher,
                        'subject' :associated_subject,
                        'batch'   :associated_batch,
                        'records' :temp_records,
                        'last_student_id':temp_records[-1]["student"].student_id
                    })
        elif data.get('submit-check',0) == 'submit-check-record':
            record = SubmissionRecord.objects.filter(submission_id=check_id).first()
            if not record:
                submission_id = 'sub_' + str(get_max_id_function(SubmissionRecord, 'submission_id') + 1)
                record = SubmissionRecord.objects.create(
                    submission_id =  submission_id,
                    associated_teacher = associated_teacher,
                    associated_subject = associated_subject,
                    associated_batch   = associated_batch
                )
                for now_updating_student in Student.objects.filter(batch = associated_batch):
                    NotebookSubmission.objects.create(
                        submission_id = record,
                        student = now_updating_student
                    )
            if data.get('sub-context',0):
                record.subject_context = data.get('sub-context')
                record.save()

            list_records = NotebookSubmission.objects.filter(submission_id = record)
            for now_updating_record in list_records:
                if data.get(f"student-{now_updating_record.student.student_id}-c-nb"):
                    now_updating_record.checked_date = data.get(f"student-{now_updating_record.student.student_id}-date") or None
                else:
                    now_updating_record.checked_date = None
                if data.get(f"student-{now_updating_record.student.student_id}-ic-nb"):
                    now_updating_record.incomplete_date = data.get(f"student-{now_updating_record.student.student_id}-date") or None
                else:
                    now_updating_record.incomplete_date = None
                now_updating_record.save()

            return HttpResponseRedirect('list_checks')
    else:
        record = SubmissionRecord.objects.filter(submission_id=check_id).first()   
        records = NotebookSubmission.objects.filter(submission_id=record).order_by('student__roll_number')
        if record:
            return render(request, 'nb_checks/nb_checking.html', {
                        'submission_record': record,
                        'teacher' :record.associated_teacher,
                        'subject' :record.associated_subject,
                        'batch'   :record.associated_batch,
                        'records' :records,
                        'last_student_id':records.last().student.student_id
                    })
        return list_checks(request)    



from django.utils.dateparse import parse_date

def student_checks_detail(request, student_id):
    if request.method == "POST":
        data = request.POST
        this_student = Student.objects.filter(student_id=student_id).first()

        for key in data:
            if data[key] and key.startswith('submission_id'):
                submission_id = data[key]
                this_submission = SubmissionRecord.objects.filter(submission_id=submission_id).first()

                # Extract and clean date values
                checked_val = data.get(f"checked_date_{submission_id}") or None
                incomplete_val = data.get(f"incomplete_date_{submission_id}") or None

                # Convert empty string to None, ensure valid date object
                checked_date = parse_date(checked_val) if checked_val else None
                incomplete_date = parse_date(incomplete_val) if incomplete_val else None

                # Update the record
                NotebookSubmission.objects.filter(
                    submission_id=this_submission, 
                    student=this_student
                ).update(
                    checked_date=checked_date,
                    incomplete_date=incomplete_date
                )

    student = Student.objects.filter(student_id=student_id).first()
    return render(request, 'nb_checks/student_checks_detail.html', {
        'student': student,
        'records': NotebookSubmission.objects.filter(student=student).order_by('submission_id__add_date'),
    })



def all_students(request):
    students_list = Student.objects.select_related('batch').all().order_by('batch__current_class', 'roll_number')
    context = {
        'student_groups' : {
            '5th': [s for s in students_list if s.batch.current_class == 5],
            '6th': [s for s in students_list if s.batch.current_class == 6],
            '7th': [s for s in students_list if s.batch.current_class == 7],
            '8th': [s for s in students_list if s.batch.current_class == 8],
            '9th': [s for s in students_list if s.batch.current_class == 9],
            '10th': [s for s in students_list if s.batch.current_class == 10]
        }
    }
    return render(request, 'nb_checks/all_students.html', context)

