from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from utils.CIR import CandidateInfoRetreival
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")

class CV_ScoringSystem:
    
    def __init__(self):
        # Set up model
        self.model = ChatOpenAI(model="gpt-4o-mini")
        
        # parsers
        self.cv_parser = CandidateInfoRetreival()
        self.json_parser = JsonOutputParser()
    
    async def get_candidate_info(self, user_cv):
      return await self.cv_parser.extractInfo(user_cv)

    def scoring_scheme(self):
        scoring_critera = {
                "weights": {
                    "Education": 20,
                    "Experience": 50,
                    "Skills": 30
                },
                "criteria": {
                    "Education": {
                    "Degree": {
                        "max_score": 4,
                        "scoring": {
                        "Bachelor's degree in relevant field": 2,
                        "Master's degree in relevant field": 2,
                        "Bachelor's degree in unrelated field": 0,
                        "No degree": 0
                        }
                    },
                    "Degree Relevance": {
                        "max_score": 2,
                        "scoring": {
                        "Highly relevant degree": 2,
                        "Somewhat relevant degree": 1,
                        "No relevant degree": 0
                        }
                    },
                    "Institution Reputation": {
                        "max_score": 2,
                        "scoring": {
                        "Well-regarded or prestigious institution in relevant field": 2,
                        "Moderately ranked institution in relevant field": 1,
                        "Unknown or low-ranked institution in relevant field": 0
                        }
                    },
                    "Academic Performance": {
                        "max_score": 2,
                        "scoring": {
                        "Excellent academic performance (CGPA above 3.5)": 2,
                        "Average academic performance (CGPA between 2.0 and 3.4)": 1,
                        "Low academic performance or no CGPA provided": 0
                        }
                    }
                    },
                    "Experience": {
                    "Job Relevance": {
                        "max_score": 5,
                        "scoring": {
                        "Directly relevant experience with the same industry, job function, and level of responsibility": 5,
                        "Relevant experience with a similar industry, job function, or level of responsibility": 4,
                        "Partially relevant experience with some transferable skills": 3,
                        "Limited relevance but some transferable skills": 2,
                        "No relevance to the position": 0
                        }
                    },
                    "Years of Experience": {
                        "max_score": 5,
                        "scoring": {
                        "7+ years of relevant experience or more": 5,
                        "5-6 years of relevant experience": 4,
                        "3-4 years of relevant experience": 3,
                        "1-2 years of relevant experience": 2,
                        "Less than 1 year of relevant experience": 1
                        }
                    },
                    "Achievements and Impact": {
                        "max_score": 5,
                        "scoring": {
                        "Consistently achieved exceptional results and made a significant impact": 5,
                        "Frequently achieved above-average results and made a noticeable impact": 4,
                        "Occasionally achieved noteworthy results and made a moderate impact": 3,
                        "Demonstrated some achievements and made a minor impact": 2,
                        "No notable achievements or impact": 0
                        }
                    },
                    "Skills and Expertise": {
                        "max_score": 5,
                        "scoring": {
                        "Possesses an extensive range of relevant skills and expertise": 5,
                        "Demonstrates a broad set of relevant skills and expertise": 4,
                        "Shows a moderate range of relevant skills and expertise": 3,
                        "Exhibits some relevant skills and expertise": 2,
                        "Lacks relevant skills and expertise": 0
                        }
                    },
                    "Progression and Growth": {
                        "max_score": 5,
                        "scoring": {
                        "Consistently demonstrated career progression and took on increasing levels of responsibility": 5,
                        "Experienced noticeable career growth and assumed greater responsibilities": 4,
                        "Showed some career advancement and took on additional responsibilities": 3,
                        "Limited career growth but demonstrated some increased responsibilities": 2,
                        "No career progression or increased responsibilities": 0
                        }
                    }
                    },
                    "Skills": {
                    "Relevance": {
                        "max_score": 2,
                        "scoring": {
                        "The skills and qualifications closely match the requirements of the job": 2,
                        "Some relevant skills and qualifications are mentioned, but there are also irrelevant ones": 1,
                        "The skills and qualifications have little to no relevance to the job": 0
                        }
                    },
                    "Depth of Expertise": {
                        "max_score": 2,
                        "scoring": {
                        "The candidate demonstrates extensive expertise in the mentioned skills and qualifications": 2,
                        "The candidate possesses a moderate level of expertise in the mentioned skills and qualifications": 1,
                        "The candidate lacks depth of expertise in the mentioned skills and qualifications": 0
                        }
                    },
                    "Years of Experience": {
                        "max_score": 2,
                        "scoring": {
                        "The candidate has a significant number of years of experience directly related to the skills and qualifications": 2,
                        "The candidate has some years of experience, but it might not be directly relevant to the skills and qualifications mentioned": 1,
                        "The candidate lacks substantial relevant experience": 0
                        }
                    }
                    }
                }
                }
        
        return scoring_critera

    def extract_weights_max_scores_and_scoring(self, score_template):
      # Extract weights
      weights = score_template.get('weights', {})
      
      # Extract max scores and scoring schemes
      max_scores = {field: 0 for field in weights}  # Initialize max scores for each field
      scoring_schemes = {}
      
      def traverse_criteria(criteria, parent_field=None):
        for key, value in criteria.items():
            if isinstance(value, dict):
                if 'max_score' in value:
                    # Aggregate max_score for the main field
                    if parent_field in max_scores:
                        max_scores[parent_field] += value['max_score']
                    # Add scoring schemes under the main field
                    if parent_field not in scoring_schemes:
                        scoring_schemes[parent_field] = {}
                    scoring_schemes[parent_field][key] = value.get('scoring', {})
                if 'scoring' in value:
                    # Stop at scoring level as it doesn't contain nested fields
                    continue
                traverse_criteria(value, parent_field or key)
      
      traverse_criteria(score_template.get('criteria', {}))
      
      return weights, max_scores, scoring_schemes
    
    def education_score_evaluation(self, candidate_cv, jd_edu, max_score, scoring_schema):
        edu_prompt = ChatPromptTemplate.from_messages([
        ("system", """
         
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, and the candidate's educational information to score it against.
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
        ),
        ("user", """
        Job Description: {jd} 
        Candidate Information: {candidate_cv}
        """
        )
    ])

        # Chain the prompt, model, and JSON output parser
        jd_chain = edu_prompt | self.model | self.json_parser
        
        response = jd_chain.invoke({"jd" : jd_edu,
                                    "candidate_cv" : candidate_cv,
                                    "scoring_schema": scoring_schema,
                                    "max_score" : max_score})
        return response
    
    def experience_score_evaluation(self, candidate_cv, jd_exp, max_score, scoring_schema):
        exp_prompt = ChatPromptTemplate.from_messages([
        ("system", """
         
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, and the candidate's experience information to score it against.
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
        ),
        ("user", """
        Job Description: {jd} 
        Candidate Information: {candidate_cv}
        """
        )
    ])

        # Chain the prompt, model, and JSON output parser
        jd_chain = exp_prompt | self.model | self.json_parser
        
        response = jd_chain.invoke({"jd" : jd_exp,
                                    "candidate_cv" : candidate_cv,
                                    "scoring_schema": scoring_schema,
                                    "max_score" : max_score})
        return response

    def skill_score_evaluation(self, candidate_cv, jd_skill, max_score, scoring_schema):
        exp_prompt = ChatPromptTemplate.from_messages([
        ("system", """
         
        You are an expert at evaluating job descriptions against a scoring schema. 
        You will be provided with a job description, and the candidate's skill information to score it against.
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
        ),
        ("user", """
        Job Description: {jd} 
        Candidate Information: {candidate_cv}
        """
        )
    ])

        # Chain the prompt, model, and JSON output parser
        jd_chain = exp_prompt | self.model | self.json_parser
        
        response = jd_chain.invoke({"jd" : jd_skill,
                                    "candidate_cv" : candidate_cv,
                                    "scoring_schema": scoring_schema,
                                    "max_score" : max_score})
        return response
    
ranking = CV_ScoringSystem()

def get_scoring_critera():
    return ranking.scoring_scheme()

def get_max_scores_and_scoring(scoring_scheme):
    weights, max_scores, scoring_schemes = ranking.extract_weights_max_scores_and_scoring(scoring_scheme)
    return weights, max_scores, scoring_schemes 
    