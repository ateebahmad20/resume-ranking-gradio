# Resume Ranking 
 
- **Description:**
The Resume Ranking Tool that is built on Gradio allows users to assess and rank candidates by matching their resumes with a provided job description. The tool uses advanced algorithms to evaluate CVs against various dynamic scoring criterias, providing a clear ranking of the most suitable candidates for the job.

- **Functionalities:**
  - **Resume Upload:**
    Users can upload multiple CVs in various formats (PDF, DOCX, TXT) and evaluate them against a specified job description.
  - **Job Description Input:**
    Users can input the job description for the position, which the tool will use to evaluate and rank candidates based on relevance and alignment with the job requirements.
  - **Resume Scoring:**
    The tool assesses resumes based on a dynamic scoring criteria, such as education, experience, and skills, and generates a score for each candidate. This scoring is flexible and can be adjusted based on the job description.
  - **Scoring Scheme Customization:**
    Administrators or users can customize the scoring criteria and weights to match specific needs, ensuring the evaluation process aligns with organizational priorities.
  - **User-friendly Interface:**
    The app provides an intuitive interface where users can easily upload resumes, view results, and analyze candidate rankings. The tool is designed to enhance the hiring process by offering a data-driven approach to resume screening.
  - **Result Visualization:**
    After ranking the resumes, the app presents a detailed and well-organized result table, showcasing the scores and analysis behind each candidate’s ranking.


## Setup Instructions

### Manual Setup (Using Conda Environment)

1. Create a Conda environment named resume-ranking with Python 3.11.11:

   ```bash
   conda create -n resume-ranking python=3.13.1
   ```
2. Activate the conda environment.

   ```bash
   conda activate resume-ranking 
   ```
3. Install all the required modules listed in requirement.txt:

   ```bash
   pip install -r ./requirement.txt
   ```

### Launching the Gradio App

Once all the dependencies are installed, you can launch the app locally:

```bash
python gradio_app.py
```
