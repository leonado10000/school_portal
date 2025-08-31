from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Batch
from django.db import IntegrityError

def class_list(request):
    """
    Display all batches/classes with links to their students.
    """
    batches = Batch.objects.all().order_by('current_class', 'batch_id')

    return render(request, 'students/class_list.html', {
        'batches': batches
    })


# View one student
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, "students/student_detail.html", {"student": student})


# Add new student
def student_create(request):
    batches = Batch.objects.all()
    form_data = {}
    error = None

    if request.method == "POST":
        form_data = request.POST.dict()
        try:
            student = Student(
                student_id=form_data.get("student_id", "").strip(),
                roll_number=form_data.get("roll_number") or 0,
                name=form_data.get("name", "").strip(),
                batch_id=form_data.get("batch") or 1,
                school_id=form_data.get("school") or 1,
                fathers_name=form_data.get("fathers_name") or None,
                mothers_name=form_data.get("mothers_name") or None,
                date_of_birth=form_data.get("date_of_birth") or None,
                contact_number=form_data.get("contact_number") or None,
                address=form_data.get("address") or None,
            )
            student.save()
            return redirect("student_detail", student_id=student.pk)
        except IntegrityError:
            error = "Student with that student_id already exists."
    # pass student=None so template uses form_data if present
    return render(
        request,
        "students/student_form.html",
        {"batches": batches, "student": None, "form_data": form_data, "error": error},
    )


# Edit existing student
def student_edit(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    batches = Batch.objects.all()
    form_data = {}
    error = None

    if request.method == "POST":
        form_data = request.POST.dict()
        try:
            student.student_id = form_data.get("student_id", student.student_id).strip()
            student.roll_number = form_data.get("roll_number") or student.roll_number
            student.name = form_data.get("name", student.name).strip()
            student.batch_id = form_data.get("batch") or student.batch_id
            student.school_id = form_data.get("school") or student.school_id
            student.fathers_name = form_data.get("fathers_name") or None
            student.mothers_name = form_data.get("mothers_name") or None
            student.date_of_birth = form_data.get("date_of_birth") or None
            student.contact_number = form_data.get("contact_number") or None
            student.address = form_data.get("address") or None
            student.save()
            return redirect("student_detail", student_id=student.pk)
        except IntegrityError:
            error = "Could not save — student_id may already exist."

    return render(
        request,
        "students/student_form.html",
        {"batches": batches, "student": student, "form_data": form_data, "error": error},
    )


# Delete student
def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})


def student_list_by_batch(request, batch_id):
    """
    Display all students belonging to a specific batch.
    """
    batch = get_object_or_404(Batch, id=batch_id)
    students = Student.objects.filter(batch=batch).order_by('roll_number')

    return render(request, 'students/student_list.html', {
        'batch': batch,
        'students': students
    })