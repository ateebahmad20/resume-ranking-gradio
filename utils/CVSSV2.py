import json
from openai import OpenAI
import pandas as pd
from utils.prompts import CVsScoringPrompt
import uuid
import os
import aiohttp
import asyncio
from utils.CV_ranking import get_max_scores_and_scoring

from dotenv import load_dotenv
load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class CVScoringSystem():
    def __init__(self):
        self.fname = ""
        self.promptCVS = CVsScoringPrompt()

    async def send_request(self, prompt):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": prompt,
                    "temperature": 0
                }
            ) as response:
                result = await response.json()
                return result['choices'][0]['message']['content']
            
    async def cvRankingV3(self, job_desc, api_data, scoring_scheme):
        data_all_cvs = []

        # Extract scoring configuration dynamically
        weights, max_scores, scoring_schemes = get_max_scores_and_scoring(scoring_scheme)
        categories = list(weights.keys())  # Extract all user-defined categories

        all_prompts = []
        for cv in range(len(api_data)):
            prompts = []
            for category in categories:
                candidate_data = api_data[cv].get(category.lower(), api_data[cv])
                scoring_scheme = api_data[cv].get(category.lower(), api_data[cv])
                prompts.append(self.promptCVS.promptTemplate(candidate_data, job_desc, max_scores[category], scoring_schemes[category], category))

            # Add the relevance summary prompt
            prompts.append(self.promptCVS.promptRelevanceSummary(api_data[cv], job_desc))
            all_prompts.append(prompts)

        # Asynchronously request all prompts for all CVs
        responses = await asyncio.gather(*[
            asyncio.gather(*[self.send_request(prompt) for prompt in prompts]) for prompts in all_prompts
        ])

        for cv, cv_responses in zip(range(len(api_data)), responses):
            talent_id = api_data[cv].get("education", [{}])[0].get("talent_id")

            cv_score = {
                "id": talent_id or str(uuid.uuid4()),
                "name": api_data[cv]["name"],
                "score": 0,
                "description": "",
            }

            category_scores = {}
            for res, category in zip(cv_responses[:-1], categories):  # Exclude last response (description)
                print(res)
                parsed_response = json.loads(res)
                score_key = f"{category} Score"
                category_score = parsed_response.get(score_key, 0)
                category_scores[category.lower()] = int(category_score / max_scores[category] * 100)

            # Extract description
            parsed_desc = json.loads(cv_responses[-1])  # Last response is the description
            cv_score["description"] = parsed_desc.get("Description", "")

            # Weighted scoring calculation
            total_weighted_score = sum(
                weights[category] * (category_scores[category.lower()] / 100) for category in categories
            )

            cv_score.update(category_scores)
            cv_score["score"] = round(float(total_weighted_score), 1)

            data_all_cvs.append(cv_score)

        # Sorting and final ranking
        data_all_cvs = sorted(data_all_cvs, key=lambda x: x["score"], reverse=True)
        return data_all_cvs

      
    # async def cvRankingV3(self, job_desc, api_data, scoring_scheme):
    #     ranking = [["cv_id", "score"]]
    #     data_all_cvs = []

    #     weights, max_scores, scoring_schemes = get_max_scores_and_scoring(scoring_scheme)

    #     all_prompts = []
    #     for cv in range(len(api_data)):
    #         prompts = [
    #             self.promptCVS.promptEducation(api_data[cv]["education"], job_desc, max_scores['Education'], scoring_schemes['Education']),
    #             self.promptCVS.promptExperience(api_data[cv]["experience"], job_desc, max_scores['Experience'], scoring_schemes['Experience']),
    #             self.promptCVS.promptSkills(api_data[cv]["skills"], job_desc,  max_scores['Skills'], scoring_schemes['Skills']),
    #             self.promptCVS.promptRelevanceSummary(api_data[cv], job_desc)
    #         ]
    #         all_prompts.append(prompts)  # Add the set of prompts for this CV to the list

    #     # Asynchronously request all prompts for all CVs concurrently
    #     responses = await asyncio.gather(*[
    #         asyncio.gather(*[self.send_request(prompt) for prompt in prompts]) for prompts in all_prompts
    #     ])
        
    #     # Process each CV's responses
    #     for cv, cv_responses in zip(range(len(api_data)), responses):
    #         talent_id = api_data[cv]["education"][0].get("talent_id")
            
    #         print(api_data[cv]["name"], cv_responses)

    #         cv_score = {
    #             "id": None,
    #             "name": api_data[cv]["name"],
    #             "score": 0,
    #             "edu_score": 0,
    #             "skill_score": 0,
    #             "exp_score": 0,
    #             "description": ""
    #         }

    #         # Handle missing talent_id
    #         if talent_id:
    #             cv_score["id"] = talent_id
    #         else:
    #             cv_score["id"] = str(uuid.uuid4())
            
    #         # Process responses for the current CV
    #         for res, section in zip(cv_responses, ["Education", "Experience", "Skills", "Description"]):
    #             parsed_response = json.loads(res)
    #             if section == "Education":
    #                 cv_score["edu_score"] = parsed_response.get("Education Score", 0)
    #             elif section == "Experience":
    #                 cv_score["exp_score"] = parsed_response.get("Experience Score", 0)
    #             elif section == "Skills":
    #                 cv_score["skill_score"] = parsed_response.get("Skill Score", 0)
    #             elif section == "Description":
    #                 cv_score["description"] = parsed_response.get("Description", "")

    #         # Calculate weighted total score
    #         edu_weight = weights["Education"] * (cv_score["edu_score"] / max_scores["Education"])
    #         exp_weight = weights["Experience"] * (cv_score["exp_score"] / max_scores["Experience"])
    #         skill_weight = weights["Skills"] * (cv_score["skill_score"] / max_scores["Skills"])
            
    #         cv_score["edu_score"] = int(cv_score["edu_score"] / max_scores["Education"] * 100)
    #         cv_score["exp_score"] = int(cv_score["exp_score"] / max_scores["Experience"] * 100)
    #         cv_score["skill_score"] = int(cv_score["skill_score"] / max_scores["Skills"] * 100)

    #         cv_score["score"] = edu_weight + exp_weight + skill_weight
    #         data_all_cvs.append(cv_score)

    #         # Add to ranking list
    #         ranking.append([cv_score["id"], cv_score["score"]])

    #     # Sort data_all_cvs by the score in descending order
    #     data_all_cvs = sorted(data_all_cvs, key=lambda x: x["score"], reverse=True)

    #     # Update the ranking list based on the sorted data
    #     ranking = [[cv["name"], cv["score"]] for cv in data_all_cvs]

    #     # Create the JSON object for the final result
    #     return data_all_cvs 
    
        
