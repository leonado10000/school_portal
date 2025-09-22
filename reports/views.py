# views.py
from django.shortcuts import render
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from notebooks.models import NotebookSubmission, SubmissionRecord, Batch
from people.models import Student

@login_required(login_url='/login')
def notebook_report(request):
    """
    Notebook checking report:
    - accepts optional GET params: start_date, end_date (YYYY-MM-DD), batch (batch id), top_n (int)
    - returns: total_records, class_stats, best_ten, worst_ten, batches (for filter UI)
    """

    # parse filters from GET
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    batch_filter = request.GET.get("batch")  # expecting Batch.pk (id)
    try:
        top_n = int(request.GET.get("top_n", 10))
    except ValueError:
        top_n = 10

    # build a Q() filter for NotebookSubmission based on SubmissionRecord.add_date
    date_q = Q()
    if start:
        sd = parse_date(start)
        if sd:
            date_q &= Q(submission_id__add_date__gte=sd)
    if end:
        ed = parse_date(end)
        if ed:
            date_q &= Q(submission_id__add_date__lte=ed)

    # add batch filter (student -> batch)
    batch_q = Q()
    if batch_filter:
        try:
            bid = int(batch_filter)
            batch_q = Q(student__batch__id=bid)
        except ValueError:
            # if a non-int was passed, ignore it
            batch_q = Q()

    master_filter = date_q & batch_q

    # total records in the filtered set
    total_records = NotebookSubmission.objects.filter(master_filter).count()

    # class-wise aggregation (one query grouped by batch)
    batch_aggregation = (
        NotebookSubmission.objects.filter(master_filter)
        .values("student__batch", "student__batch__batch_id", "student__batch__current_class")
        .annotate(total=Count("id"), checked=Count("id", filter=Q(checked_date__isnull=False)))
    )

    # map batch id -> stats for quick lookup
    batch_map = {}
    for b in batch_aggregation:
        bid = b["student__batch"]
        total = b["total"]
        checked = b["checked"]
        rate = (checked / total) if total else 0.0
        batch_map[bid] = {
            "batch_id": bid,
            "label": b.get("student__batch__batch_id") or str(bid),
            "current_class": b.get("student__batch__current_class"),
            "total": total,
            "checked": checked,
            "rate": rate,
            "rate_percent": round(rate * 100, 1),
        }

    # ensure every Batch is present in class_stats (even if zero)
    class_stats = []
    for batch in Batch.objects.all().order_by("batch_id"):
        stats = batch_map.get(batch.id, None)
        if stats:
            class_stats.append(stats)
        else:
            class_stats.append({
                "batch_id": batch.id,
                "label": str(batch),
                "current_class": batch.current_class,
                "total": 0,
                "checked": 0,
                "rate": 0.0,
                "rate_percent": 0.0,
            })

    # student-level aggregation to get best/worst (group by student)
    student_agg_qs = (
        NotebookSubmission.objects.filter(master_filter)
        .values("student", "student__name", "student__roll_number", "student__student_id")
        .annotate(total=Count("id"), checked=Count("id", filter=Q(checked_date__isnull=False)))
        .filter(total__gt=0)  # only students who have at least one record in the window
    )

    # add computed rate with ExpressionWrapper (float)
    student_agg_qs = student_agg_qs.annotate(
        rate=ExpressionWrapper(F("checked") * 1.0 / F("total"), output_field=FloatField())
    )

    # best N by rate (descending)
    best_qs = student_agg_qs.order_by("-rate", "-checked")[:top_n]
    best_ten = []
    for s in best_qs:
        rate = float(s.get("rate") or 0.0)
        best_ten.append({
            "student_id": s["student"],
            "name": s["student__name"],
            "roll": s.get("student__roll_number"),
            "student_key": s.get("student__student_id"),
            "total": s["total"],
            "checked": s["checked"],
            "rate": rate,
            "rate_percent": round(rate * 100, 1),
        })

    # worst N by rate (ascending)
    worst_qs = student_agg_qs.order_by("rate", "-total")[:top_n]
    worst_ten = []
    for s in worst_qs:
        rate = float(s.get("rate") or 0.0)
        worst_ten.append({
            "student_id": s["student"],
            "name": s["student__name"],
            "roll": s.get("student__roll_number"),
            "student_key": s.get("student__student_id"),
            "total": s["total"],
            "checked": s["checked"],
            "rate": rate,
            "rate_percent": round(rate * 100, 1),
        })

    # batches to populate filter UI
    batches = Batch.objects.all().order_by("batch_id")

    context = {
        "total_records": total_records,
        "class_stats": class_stats,
        "best_ten": best_ten,
        "worst_ten": worst_ten,
        "batches": batches,
        # echo filters
        "filter_start": start,
        "filter_end": end,
        "filter_batch": int(batch_filter) if batch_filter and batch_filter.isdigit() else None,
        "top_n": top_n,
    }
    return render(request, "reports/notebook_report.html", context)
