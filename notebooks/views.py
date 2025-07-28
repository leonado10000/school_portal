from django.db import models
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Student, NotebookSubmission, SubmissionRecord, Subject, Teacher, Batch

print_arg = "\n sys: "
def get_max_id_function(class_name:models.Model, id_name:str):
    max_list = [int(vals[id_name].split('_')[-1]) for vals in class_name.objects.values(id_name)]
    return max(max_list) if max_list else 0

def list_checks(request):
    return render(request, 'nb_checks/list_checks.html', {
        'records' :SubmissionRecord.objects.all(),
        'batches' :Batch.objects.all(),
        'subjects':Subject.objects.all(),
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
            return render(request, 'nb_checks/nb_checking.html', {
                        'check_id':check_id,
                        'teacher' :associated_teacher,
                        'subject' :associated_subject,
                        'batch'   :associated_batch,
                        'students':Student.objects.filter(batch=associated_batch)
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
            
            list_records = NotebookSubmission.objects.filter(submission_id = record)
            print(list_records)
            print(data)
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

            return HttpResponseRedirect('/list_checks')
    else:
        # get an existing record
        record = SubmissionRecord.objects.filter(submission_id=check_id).first()   
        if record:
            return render(request, 'nb_checks/nb_checking.html', {
                        'submission_record': record,
                        'teacher' :record.associated_teacher,
                        'subject' :record.associated_subject,
                        'batch'   :record.associated_batch,
                        'records' :NotebookSubmission.objects.filter(submission_id = record)
                    })
        return list_checks(request)    



def student_checks_detail(request, student_id):
    student = Student.objects.filter(student_id=student_id).first()
    return render(request, 'nb_checks/student_checks_detail.html', {
        'student': student,
        'records': NotebookSubmission.objects.filter(student=student)
    })

