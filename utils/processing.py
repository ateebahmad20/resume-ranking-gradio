import os
import shutil

# Directory for saving uploaded files
UPLOAD_CVs = "./data/uploaded_pdfs"
UPLOAD_JDs = "./data/uploaded_jds"

os.makedirs(UPLOAD_CVs, exist_ok=True)
os.makedirs(UPLOAD_JDs, exist_ok=True)

async def process_applications(job_description, cvs):

    # Save the job description
    job_desc_file = os.path.join(UPLOAD_JDs, "job_description.txt")
    with open(job_desc_file, "w") as f:
        f.write(job_description)

    # Save the uploaded CVs
    saved_files = []
    for cv in cvs:
        filepath = os.path.join(UPLOAD_CVs, os.path.basename(cv.name))

        # Copy the file from temporary directory to the target path
        shutil.copy(cv, filepath)
        saved_files.append(filepath)

    return saved_files