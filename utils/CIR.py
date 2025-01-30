from utils.CVParser import CVParser
from utils.prompts import *
from openai import OpenAI
import concurrent.futures
import json
import time
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Access the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class JSONEvaluator():
    def __init__(self):
        self.fname = ""
        self.delimiter = "####"

    def prompt(self, data):

        system_message = """
        You are a helpful assistant, whose job is to identify problems in the JSON content and correct it. \n 
        User will provide you data in JSON format and your job will be to generate correct version of it. \n
        You will return a JSON format data that will contain information same as given in User info. 

        Instruction that needs to be followed:
        1. Correct all probelms present in JSON data
        2. Do not change fields and data
        3. If data is already correct return same data
        4. Return data in JSON format

        Must return data in JSON format
        """
        user_message = f"{self.delimiter}User Data: {data} \n{self.delimiter}"
        messages =  [
            {'role':'system', 
            'content': system_message},    
            {'role':'user', 
            'content': f"{user_message}"},  
        ] 
        return messages

    def response(self, data):
        print(data)
        print("JSON Evaluator Running............")
        prompt = self.prompt(data)
        # create a chat completion
        chat_completion = client.chat.completions.create(model="gpt-4o-mini", messages=prompt, temperature = 0)
        # print the chat completion
        response = chat_completion.choices[0].message.content
        print(response)
        json_object = json.loads(response)


        return json_object

class CandidateInfoRetreival():
    def __init__(self):
        self.fname = ""
        self.promptCV = CVParsingPrompt()
        self.parser = CVParser()
        self.evaluator = JSONEvaluator()


    def cvParse(self, fname):
        self.cv_text_raw = self.parser.parse(fname)
        return self.cv_text_raw

    async def send_request(self, messages):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-3.5-turbo-0125",
                    "messages": messages,
                    "temperature": 0
                }
            ) as response:
                            
                result = await response.json()
                return result['choices'][0]['message']['content']
    
    async def extractInfo_one(self, fname):
        
        self.fname = fname

        # Parse data
        cv_data = self.cvParse(fname)
        
        # Create prompts
        prompts = {
            'personal_info': self.promptCV.promptPersonalInfo(cv_data),
            'experience': self.promptCV.promptExperience(cv_data),
            'education': self.promptCV.promptEducation(cv_data),
            'skills': self.promptCV.promptSkills(cv_data),
            'courses_certificates': self.promptCV.promptCoursesCertificates(cv_data),
            'projects': self.promptCV.promptProjects(cv_data)
        }

        # Initialize responses with the expected order
        responses = {}
        
        # Async function to process each section
        async def process_section(section, prompt):
            try:
                response = await self.send_request(prompt)
                return section, response
            except Exception as exc:
                print(f"{section} generated an exception: {exc}")
                return section, None

        # Send all prompts concurrently
        tasks = [process_section(section, prompt) for section, prompt in prompts.items()]
        results = await asyncio.gather(*tasks)
        
        # Collect results in the responses dictionary
        for section, response in results:
            responses[section] = response

        # Combine the responses into a single JSON object
        json_object = {}
        for section in responses:
            response_text = responses[section]
            if response_text is None:
                continue
            try:
                json_data = json.loads(response_text)
            except json.JSONDecodeError:
                json_data = self.evaluator.response(response_text)
            json_object.update(json_data)
        
        # Process experience and education to add IDs
        experiences = json_object.get("experience", [])
        educations = json_object.get("education", [])
        for i, exp in enumerate(experiences):
            exp["id"] = i
        for i, edu in enumerate(educations):
            edu["id"] = i

        json_object["experience"] = experiences
        json_object["education"] = educations

        return json_object
    
    async def extractInfo(self, fname):
        self.fname = fname

        # Parse CV data
        cv_data = self.cvParse(fname)
        
        # Create a single prompt
        prompt = self.promptCV.promptCVParse(cv_data)
        
        # Send the single prompt and await response
        try:
            response_text = await self.send_request(prompt)
        except Exception as exc:
            print(f"Exception during parsing: {exc}")
            return None
        
        # Process the response and convert to JSON
        try:
            json_object = json.loads(response_text)
        except json.JSONDecodeError:
            json_object = self.evaluator.response(response_text)
        
        # Add IDs to experience and education entries
        experiences = json_object.get("experience", [])
        educations = json_object.get("education", [])
        for i, exp in enumerate(experiences):
            exp["id"] = i
        for i, edu in enumerate(educations):
            edu["id"] = i

        json_object["experience"] = experiences
        json_object["education"] = educations

        return json_object