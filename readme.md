1. Core
- School
- Subject
    - code : (Class)[Name](version)
- Batch
    - batch_id : batch_1
    - associated_school : SCHOOL

2. People
- Teacher
    - teacher_id : t_00001
- Student 
    - student_id : s_00001

2. Notebook
- SubmissionRecord
    - submission_id : sub_1
- NotebookSubmission
    - submission_id : SUBMISSIONRECORD


# for vercel deployement
requirements.txt should go in main app (school_portal folder)
static files require static url, root and dir then a collect static command and an add to urlpatterns as an url (in school_portal/urls.py)

### Trivia
1. On the nb_checking page, student records lost their roll number order after updates. Postgres (Neon serverless) doesn't guarantee order without an explicit ORDER BY.

Option 1 – Batch Re-save:
Re-save all 40 records after any update to maintain physical order.

❌ 40 DB writes per update, not efficient.

Option 2 – Sort on Read (✔️ Recommended):
Use .order_by('student__roll_number') when querying.

✅ Minimal cost (~O(n log n)), clean and scalable for small sets.

Use Option 2 for consistent and efficient ordering.