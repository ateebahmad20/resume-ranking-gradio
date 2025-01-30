class CVParsingPrompt():
    def __init__(self):
        self.delimiter = "####"
    
    # At the end provide "description": "str description" which shows the analysis of each score. Add Explanantion for each point sum points for each category accurately.
    def promptCVParse(self, cand_raw_cv_data):
        cv_format = """
{"name": "Ian Smith",
"email": "iansmith.dev@gmail.com",
"address": "47 W 13th St, New York, NY 10011, USA",
"linkedin_link": "https://www.linkedin.com/in/ian-smith-61b38b11/",
"summary": "Results-driven machine learning engineer with 5 years of experience in developing and implementing machine learning models to solve complex business problems. Proficient in Python, TensorFlow, and scikit-learn, with a deep understanding of statistical analysis and data visualization. Strong communication and collaboration skills, with a proven track record of delivering high-quality solutions on time.",
"experience": [{"job_title": "Senior Machine Learning Engineer",
    "company": "FireFly Technologies",
    "location": "Washington DC",
    "start_date": "07/2022",
    "end_date": "Present",
    "responsibilities": ["Led a team of 3 engineers in designing and implementing a deep learning model to optimize customer churn prediction, resulting in a 10% reduction in customer attrition.",
        "Developed and deployed a recommendation system using collaborative ﬁltering techniques, increasing user engagement by 15",
        "Implemented natural language processing algorithms to analyze customer feedback, leading to actionable insights for product improvement."]},
    {"job_title": "Machine Learning Engineer",
    "company": "Nimbus Pvt Ltd",
    "location": "Los Angeles",
    "start_date": "12/2021",
    "end_date": "06/2022",
    "responsibilities": ["Developed a machine learning pipeline for fraud detection, resulting in a 20% decrease in fraudulent transactions.",
        "Collaborated with cross-functional teams to build a real-time anomaly detection system using streaming data from IoT devices.",
        "Optimized and ﬁne-tuned existing models to improve accuracy and reduce model latency by 30%."]}],
"volunteer_work":[{"job_title": "Junior Machine Learning Engineer",
    "company": "Panem Technologies",
    "location": "New York",
    "start_date": "01/2021",
    "end_date": "11/2021",
    "responsibilities": ["Assisted in the development of a recommendation engine, utilizing collaborative ﬁltering and matrix factorization techniques.",
        "Conducted data preprocessing, feature engineering, and model selection to improve the accuracy of predictive models.",
        "Collaborated with the data engineering team to design and implement scalable data pipelines."]}],
"education": [{"degree": "Masters of Science in Computer Science",
    "university": "Aston University",
    "location": "Paris, France",
    "start_date": "2019",
    "end_date": "2021",
    "cgpa": "3.5"},
    {"degree": "Bachelor of Engineering in Computer Science",
    "university": "Gomal University",
    "location": "London, UK",
    "start_date": "2013",
    "end_date": "2017",
    "cgpa": "3.0"}],
"skills": ["Python",
    "Java",
    "C++",
    "TensorFlow",
    "Scikit-learn",
    "Pytorch",
    "Keras",
    "Pandas",
    "Numpy",
    "SQL"],
"courses_certificates": ["Deep Learning Specialization deeplearning.ai (Coursera)",
    "Python for Data Science  University of Michigan (Coursera)",
    "AWS Certiﬁed Machine Learning Specialty"]}
        """
        system_message = f"""
You will be provided with candidate CV raw data. \
The CV data will be delimited with \
{self.delimiter} characters.
Extract candidate profile information from given cv data. \
Provide your output in only json format with the following example format
{cv_format} 

You should follow following instructions:
    1. Return only data in above format
    2. Contain only keys mention above format

Only output the json data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information: \n {cand_raw_cv_data}{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 
        return messages

    def promptPersonalInfo(self, cand_raw_cv_data):
        system_message = f"""
        You will be provided with candidate CV raw data.
        The CV data will be delimited with {self.delimiter} characters.
        Extract the candidate's personal information from the given CV data

        Provide your output in JSON format with the following example format:
        {{
            "name": "Ian Smith",
            "email": "iansmith.dev@gmail.com",
            "address": "47 W 13th St, New York, NY 10011, USA",
            "contact number:" 123-456-7890, 
            "linkedin_link": "https://www.linkedin.com/in/ian-smith-61b38b11/",
            "github link": "https://github.com/ian-smith-61b38b11",
            "summary": "Results-driven machine learning engineer with 5 years of experience..."
        }}

        Only output the JSON data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
        return messages

    def promptExperience(self, cand_raw_cv_data):
        system_message = f"""
        You will be provided with candidate CV raw data.
        The CV data will be delimited with {self.delimiter} characters.
        Extract the candidate's work experience from the given CV data.
        Provide your output in JSON format with the following example format:
        {{
            "experience": [
                {{
                    "job_title": "Senior Machine Learning Engineer",
                    "company": "FireFly Technologies",
                    "location": "Washington DC",
                    "start_date": "07/2022",
                    "end_date": "Present",
                    "responsibilities": ["Responsibility 1", "Responsibility 2"]
                }},
                // Additional experiences
            ]
        }}
        Only output the JSON data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
        return messages

    def promptEducation(self, cand_raw_cv_data):
        system_message = f"""
        You will be provided with candidate CV raw data.
        The CV data will be delimited with {self.delimiter} characters.
        Extract the candidate's education details from the given CV data.
        Provide your output in JSON format with the following example format:
        {{
            "education": [
                {{
                    "degree": "Masters of Science in Computer Science",
                    "university": "Aston University",
                    "location": "Paris, France",
                    "start_date": "2019",
                    "end_date": "2021"
                }},
                // Additional education entries
            ]
        }}
        Only output the JSON data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
        return messages
    
    # def promptSkillsAndCertificates(self, cand_raw_cv_data):
    #     system_message = f"""
    #     You will be provided with candidate CV raw data.
    #     The CV data will be delimited with {self.delimiter} characters.
    #     Extract the candidate's skills and courses/certificates from the given CV data.

    #     Provide your output in JSON format with the following example format:
    #     {{
    #         "skills": ["Python", "Java", "C++"],
    #         "courses_certificates": ["Course 1", "Certificate 2"]
    #     }}

    #     Only output the JSON data, with nothing else.
    #     """
    #     user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
    #     messages = [
    #         {'role': 'system', 'content': system_message},
    #         {'role': 'user', 'content': user_message},
    #     ]
    #     return messages
    
    def promptSkills(self, cand_raw_cv_data):
        system_message = f"""
        You will be provided with candidate CV raw data.
        The CV data will be delimited with {self.delimiter} characters.
        Extract the candidate's skills from the given CV data.
        Provide your output in JSON format with the following example format:
        {{
            "skills": ["Python", "Java", "C++"]
        }}
        Only output the JSON data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
        return messages

    def promptCoursesCertificates(self, cand_raw_cv_data):
        system_message = f"""
        You will be provided with candidate CV raw data.
        The CV data will be delimited with {self.delimiter} characters.
        Extract the candidate's courses and certificates from the given CV data.
        
        Provide your output in JSON format with the following example format:
        {{
            "courses_certificates": ["Course 1", "Certificate 2"]
        }}
        
        Only output the JSON data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
        return messages
    
    def promptProjects(self, cand_raw_cv_data):
        system_message = f"""
        You will be provided with candidate CV raw data.
        The CV data will be delimited with {self.delimiter} characters.
        Extract the candidate's Projects from the given CV data.
        
        Provide your output in JSON format with the following example format:
        {{
            "Projects": [
                {{
                    "Project Title": "Gym Reservation Bot",
                    "start_date": "07/2022",
                    "end_date": "Present",
                    "responsibilities": ["Responsibility 1", "Responsibility 2"]
                }},
                // Additional projects
            ]
        }}
        
        Only output the JSON data, with nothing else.
        """
        user_message = f"{self.delimiter} Candidate Raw CV Information:\n{cand_raw_cv_data}\n{self.delimiter}"
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_message},
        ]
        return messages

class CVsScoringPrompt():
    def __init__(self):
        self.delimiter = "####"
    
    def promptTemplate(self, candidate_data, job_desc, max_score, scoring_schema, category):
        system_message = f"""
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, candidate's {category} information, and a scoring scheme to score it against.
        Your task is to evaluate the provided job description against the CV and output a structured JSON object containing the following field:
        **keys**: 
        - {category} Score: This is the total score you gave to the candidate based on the job description
        - Scoring Criteria: This is the thought process you used to give scores to the candidate based on the job description
        
        Scoring Schema:
        {scoring_schema}
        
        Note:
        - You should keep in mind that the scoring should never exceed the max scores defined for that criteria:
        {max_score}
        
        Only return the JSON data with no additional text or formatting (such as ```json). 
        """
        user_message = f"{self.delimiter}Job Description: \n {job_desc} \n {self.delimiter} Candidate Information: \n {candidate_data}{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 

        return messages

    def promptEducation(self, candidate_data, job_desc, max_score, scoring_schema):
        system_message = f"""
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, candidate's educational information, and a scoring scheme to score it against.
        Your task is to evaluate the provided job description against the CV and output a structured JSON object containing the following field:
        **keys**: 
        - Education Score: This is the total score you gave to the candidate based on the job description
        - Scoring Criteria: This is the thought process you used to give scores to the candidate based on the job description
        
        Scoring Schema:
        {scoring_schema}
        
        Note:
        - You should keep in mind that the scoring should never exceed the max scores defined for that criteria:
        {max_score}
        
        Only output the json data, with nothing else.
        """
        user_message = f"{self.delimiter}Job Description: \n {job_desc} \n {self.delimiter} Candidate Information: \n {candidate_data}{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 

        return messages
    
    def promptExperience(self, candidate_data, job_desc, max_score, scoring_schema):
        system_message = f"""
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, candidate's experience information, and a scoring scheme to score it against.
        Your task is to evaluate the provided job description against the CV and output a structured JSON object containing the following field:
        **keys**: 
        - Experience Score: This is the total score you gave to the candidate based on the job description
        - Scoring Criteria: This is the thought process you used to give scores to the candidate based on the job description
        
        Scoring Schema:
        {scoring_schema}
        
        Note:
        - You should keep in mind that the scoring should never exceed the max scores defined for that criteria:
        {max_score}
        
        Only output the json data, with nothing else.
        """

        user_message = f"{self.delimiter}Job Description: \n {job_desc} \n {self.delimiter} Candidate Information: \n {candidate_data}{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 
        return messages
    
    def promptSkills(self, candidate_data, job_desc, max_score, scoring_schema):
        system_message = f"""
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, candidate's skill information, and the scoring scheme to score it against.
        Your task is to evaluate the provided job description against the CV and output a structured JSON object containing the following field:
        **keys**: 
        - Skill Score: This is the total score you gave to the candidate based on the job description
        - Scoring Criteria: This is the thought process you used to give scores to the candidate based on the job description
        
        Scoring Schema:
        {scoring_schema}
        
        Note:
        - You should keep in mind that the scoring should never exceed the max scores defined for that criteria:
        {max_score}
        
        Only output the json data, with nothing else.
        """
        user_message = f"{self.delimiter}Job Description: \n {job_desc} \n {self.delimiter} Candidate Information: \n {candidate_data}{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 
        return messages

    def promptAdvance(self, candidate_data, job_desc):
        system_message = f"""
You will be provided with CV scoring scheme, candidate CV and Job description. \
The CV and Job description data will be delimited with \
{self.delimiter} characters.
Score CV based on every points mentioned in provided scheme. 
Add Explanantion for each point sum points for each category accurately. 
Provide your output in only json format with the \
keys: Total_Score, Education_Score, Work_Experience_Score, Skills_and_Qualification_Score, Achievements_and_Awards_Score, and Personal_Projects_and_Contributions_Score. 
Scoring Scheme: 
    Education (Total 20 points):
        1. Award points based on the candidate's level of education. (MS 1 points , BS 4 points)
        2. Assign higher points for degrees directly related to the job requirement degree. (5 points)
        3. If candidate university is in top 10 of QS ranking assign 10 points else 0. (10 points)
    Work Experience (Total 30 points):
        1. Allocate points based on the number of years of experience in the field.
        2. Assign higher points for experience in roles similar to the job position.
        3. Consider the depth and breadth of responsibilities, as well as the impact of the candidate's work.
    Skills and Qualifications (Total 20 points):
        1. Assess the candidate's skills and qualifications relevant to the job requirements.
        2. Assign points for technical skills, software proficiency, language fluency, and any other relevant abilities.
        3. Give extra points for specialized or in-demand skills.
    Achievements and Awards (Total 10 points):
        1. Consider any notable achievements, awards, or recognition received by the candidate.
        2. If there is no achievement mentions reward 0 points.
    Personal Projects and Contributions (Total 10 points):
        1. Evaluate any personal projects, open-source contributions, or relevant initiatives undertaken by the candidate.
        2. Assign points based on the impact, creativity, and relevance of these projects.
        3. If there is no relevant project mentions reward 0 points for Personal Projects and Contributions.

Only output the json data, with nothing else.
        """
        user_message = f"{self.delimiter}Job Description: \n {job_desc} \n {self.delimiter} Candidate Information: \n {candidate_data}{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 
        return messages

    def promptRelevanceSummary(self, candidate_data, job_desc):
        system_message = """
        You will be provided with a candidate's CV and a Job description. 
        Analyze the candidate's qualifications, experience, and skills, and explain in a brief summary why this candidate is or is not relevant to the provided job description. 
        Your explanation should be concise and focus on key points like education, experience, and skills relevant to the job.
        Provide your output strictly in the following JSON format:

        output format:
        {
            "Description": "The candidate is highly relevant for the job due to their extensive experience and skills in the field."
        }

        example output:
        {
            "Description": "The candidate is a good match as they have 5 years of experience in the field, strong problem-solving skills, and relevant certifications."
        }
        """
        
        user_message = f"{self.delimiter}Job Description: \n{job_desc}\n{self.delimiter}Candidate Information: \n{candidate_data}{self.delimiter}"
        
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{user_message}"}
        ]
        
        return messages
    
    def job_des_to_json(self, job_des):
        system_message = """
You are tasked with extracting relevant information from a job description to create a structured JSON output. Your goal is to extract only three categories: skills, education, and experience. For each category:

Skills: Extract technologies, frameworks, programming languages, tools, and any specific abilities mentioned in the job description.
Education: Extract relevant educational qualifications, degrees, or related fields of study.
Experience: Extract any information related to required work experience, number of years, and specific roles or tasks the candidate is expected to have experience with.
Output the extracted information in the following JSON format:
{
"skills": [
    // List of extracted skills and technologies
],
"education": [
    // Extracted educational qualifications
],
"experience": [
    // Extracted work experience details
]}
"""
        
        user_message = f"{self.delimiter}Job Description: \n{job_des}\n"
        
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{user_message}"}
        ]
        
        return messages
    
    def score_experience(self, job_desc, candidate_experiance):
        system_message = """
You are a language model tasked with evaluating candidate experience based on job descriptions. Your job is to compare the candidate's experience against the job requirements provided, and return a JSON object. The output should be structured strictly as a JSON, and the keys of the output should exactly match the experience requirements in the job description.

The experience requirements in the job description will be provided as a list, and your output must include a corresponding boolean value for each key, where True indicates the candidate meets the requirement, and False indicates they do not.
The candidate experience and Job description data will be delimited with \
{self.delimiter} characters.
Here are the specific rules:

Only output JSON.
Use the keys provided in the job description without modification.
Return True if the candidate's experience matches a requirement, otherwise return False 

Example input job description:
{
    "experience": [
        "3+ years of experience in front-end development",
        "Proven track record of delivering live products",
        "Experience in leading front-end development teams"
    ]
}

Example output:
{
    "3+ years of experience in front-end development": True,
    "Proven track record of delivering live products": True,
    "Experience in leading front-end development teams": False
}

Ensure that the output keys remain identical to those in the job description provided.
"""
        
        user_message = f"{self.delimiter}Job Description: \n{job_desc}\n{self.delimiter}Candidate experience: \n{candidate_experiance}{self.delimiter}"
        
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{user_message}"}
        ]
        
        return messages
        
    def score_education(self, job_desc, candidate_education):
        system_message = """
        
You are a language model tasked with evaluating candidate education based on job descriptions. Your job is to compare the candidate's education against the job requirements provided, and return a JSON object. The output should be structured strictly as a JSON, and the keys of the output should exactly match the education requirements in the job description.

The education requirements in the job description will be provided as a list, and your output must include a corresponding boolean value for each key, where True indicates the candidate meets the requirement, and False indicates they do not.
The candidate education and Job description data will be delimited with 
{self.delimiter} characters.
Here are the specific rules:

Only output JSON.
Use the keys provided in the job description without modification.
Return True if the candidate's education matches a requirement, otherwise return False.
Example input job description:
{
    "education": [
        "Bachelor's degree in Computer Science or Related field"
    ]
}

Candidate education:
[
    {
        "degree": "Bachelor of Science in Computer Science",
        "university": "University / National Textile University",
        "start_date": "2019",
        "end_date": "2023",
        "id": 0
    },
    {
        "degree": "HSSC, PRE-ENGINEERING",
        "university": "College / Students INN College",
        "start_date": "2017",
        "end_date": "2019",
        "id": 1
    }
]

Example output:
{
    "Bachelor's degree in Computer Science or Related field": True
}

Ensure that the output keys remain identical to those in the job description provided.
     
        """
        
        user_message = f"{self.delimiter}Job Description: \n{job_desc}\n{self.delimiter}Candidate education: \n{candidate_education}{self.delimiter}"
        
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{user_message}"}
        ]
        
        return messages

    def score_skill(self, job_desc, candidate_skill):
        system_message = """
        
You are a language model tasked with evaluating candidate skills based on job descriptions. Your job is to compare the candidate's skills against the job requirements provided, and return a JSON object. The output should be structured strictly as a JSON, and the keys of the output should exactly match the skills required in the job description.

The skills requirements in the job description will be provided as a list, and your output must include a corresponding boolean value for each key, where True indicates the candidate meets the requirement, and False indicates they do not.
The candidate education and Job description data will be delimited with 
{self.delimiter} characters.
Here are the specific rules:

Only output JSON.
Use the keys provided in the job description without modification.
Return True if the candidate's skills match a requirement, otherwise return False.
Example input job description:

{
    "skills": [
    "React.js",
    "HTML",
    "CSS",
    "JavaScript",
    "Bootstrap",
    "Node.js",
    "API integration",
    "WordPress",
    "WooCommerce",
    "CI/CD pipelines",
    "Python",
    "AI-driven applications"
],
}

candidate skills:

[
    "React",
    "JavaScript",
    "HTML",
    "CSS",
    "RESTful APIs"
]

Example output:

{
    "React.js":True,
    "HTML":True,
    "CSS":True,
    "JavaScript":True,
    "Bootstrap":True,
    "Node.js":True,
    "API integration":True,
    "WordPress":True,
    "WooCommerce:True",
    "CI/CD pipelines:True",
    "Python":True,
    "AI-driven applications":True
}

Ensure that the output keys remain identical to those in the job description provided.
  """
        
        user_message = f"{self.delimiter}Job Description: \n{job_desc}\n{self.delimiter}Candidate skill: \n{candidate_skill}{self.delimiter}"
        
        messages = [
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': f"{user_message}"}
        ]
        
        return messages

class ChatBotPrompt():
    def __init__(self):
        self.delimiter = "####"
    
    def prompt(self, customer_message):
        output_format = """
{"intent": "Schedule_Event",
"entites": {"Event_Title": "Meeting with Marketing Team",
            "Event_Date": "26/09/2023",
            "Event_Time": "09:16",
            "Event_Duration": "30 minutes",
            "Event_Location": "Online",
            "Event_Description": "Discuss new marketing strategies"},
"response_to_customer": "Once you provide all the necessary information, I will create the event on your Google Calendar.",
        """
        system_message = f"""
You are a helpful and kind AI Assistant. \
Whose roles are to identify intent of the customer, extract entities from customer messages \
and ask customer to provide necessary information related to intent.  
The customer query and previous conversation will be delimited with four hashtags,\
i.e. {self.delimiter}. 
The list of intents and their respective necessary entities are given below
1. Schedule_Event: Schedule an event on Google calender
    Event_Title: Please enter a descriptive title for your event.
        Example: "Meeting with Marketing Team"
    Event_Date: Specify the date for event.
    Event_Time: Specify time for event. You can enter it in any common format, or use natural language phrases like "tomorrow at 2 PM" or "next Monday at 10:30 AM".
    Event_Duration: How long will the event last? Please mention the duration in hours or minutes.
        Example: "1 hour" or "30 minutes"
    Event_Location (optional): If the event has a physical location, please provide the address or venue name. If it's an online event, you can mention it as "Online" or provide a virtual meeting link.
    Event_Description (optional): If you would like to add any additional details or notes about the event, please provide them here.

Provide your output in only json format with the following example format
{output_format}
Instructions:
i. Ask customer to provide necessary information related to respective intent. 
ii. Maintain json file contain information related to entities, intent and response message to customer from assistant. 
iii. If customer switch its intent reset entities
iv. In start introduce yourself nicely.
v. For new line use \\n


Only output the valid json data, with nothing else.
        """
        user_message = f"{self.delimiter}Customer: {customer_message} \n{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 
        return messages


    