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