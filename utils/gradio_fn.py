import gradio as gr
from utils.CIR import CandidateInfoRetreival
from utils.CVSSV2 import CVScoringSystem
from utils.processing import process_applications
import json
import os
import time
import asyncio

output_dir = "./data/custom_scoring_scheme"
os.makedirs(output_dir, exist_ok=True)

scoring = CVScoringSystem()
retrieval = CandidateInfoRetreival()

def scores_visibility_on():
    return [gr.update(visible=True)] * 4 

def scores_visibility_off():
    return [gr.update(visible=False)] * 6

def rank_visibility_off():
    return [gr.update(visible=False)] * 2

def toggle_processing_visibility():
    return gr.update(visible=True), gr.update(visible=False)

def format_cv_scores(cv_scores):
    # Extract dynamic field names from the first candidate entry
    if not cv_scores:
        return [], []

    # Ensure description is always the last field
    field_names = ["name", "score"] + [key for key in cv_scores[0] if key not in ["id", "name", "score", "description"]] + ["description"]
    
    formatted_scores = [
        [candidate.get(field, "N/A") for field in field_names] for candidate in cv_scores
    ]

    return formatted_scores, field_names

def display_cv_scores(cv_scores, field_names):
    # Create a stunning HTML layout for the CV results
    html_output = """
    <div style="font-family: Arial, sans-serif; border: 1px solid #ddd; border-radius: 8px; padding: 20px;">
        <h2 style="text-align: center; color: #2c3e50;">CV Scoring Results</h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
            <thead>
                <tr style="background-color: #f2f2f2;">
    """
    
    # Add table headers dynamically based on field names
    for field in field_names:
        html_output += f'<th style="padding: 12px; text-align: left; font-size: 16px; font-weight: bold;">{field.replace("_", " ").title()}</th>'

    html_output += "</tr></thead><tbody>"

    # Add table rows dynamically
    for candidate in cv_scores:
        html_output += "<tr style='background-color: #fff; border-bottom: 1px solid #ddd;'>"
        
        for idx, field in enumerate(candidate):
            # Apply consistent styling for all cells
            cell_style = 'padding: 12px; font-size: 14px;'

            # Apply green color to the score field (assuming it is at index 1)
            if idx == 1:  
                html_output += f'<td style="{cell_style} color: #2ecc71;">{field}</td>'
            # Apply gray color to the description field (assuming it is the last column)
            elif idx == len(candidate) - 1:
                html_output += f'<td style="{cell_style} color: #7f8c8d;">{field}</td>'
            else:
                html_output += f'<td style="{cell_style}">{field}</td>'
        
        html_output += "</tr>"

    html_output += """
            </tbody>
        </table>
    </div>
    """

    return html_output

async def bulk_rank(job_desc, uploaded_cvs):
    # Processing CVs
    cv_files = await process_applications(job_desc, uploaded_cvs)
    tasks = [retrieval.extractInfo(file_path) for file_path in cv_files]

    start = time.time()
    all_cvs_extracted_json = await asyncio.gather(*tasks)
    print('Time Taken for Extracting: ', time.time() - start) 

    # Load scoring scheme
    with open(f"{output_dir}/scoring_scheme.json", "r") as json_file:
        scheme = json.load(json_file)

    start = time.time()
    cv_scores = await scoring.cvRankingV3(job_desc, all_cvs_extracted_json, scheme)
    print('Time Taken for Scoring: ', time.time() - start) 

    formatted_scores, field_names = format_cv_scores(cv_scores)
    html = display_cv_scores(formatted_scores, field_names)

    return (
        html,
        gr.update(visible=False),  # Hide loading message
        gr.update(visible=True),  # Show CV results table
    )

def load_weights():

    # loading the scoring scheme
    with open(f"{output_dir}/scoring_scheme.json", "r") as json_file:
        scoring_scheme = json.load(json_file)  # Parse the JSON content into a Python dictionary

    weights = [[category, weight] for category, weight in scoring_scheme["weights"].items()]
    return weights

def load_nested_criterias(scheme):
    formatted_criteria = []

    # Iterate through the criteria dictionary
    for category, sub_criteria in scheme["criteria"].items():
        for criterion, details in sub_criteria.items():
            # Extract descriptions and scores into separate lines
            descriptions = list(details["scoring"].keys())
            scores = list(details["scoring"].values())

            # Create rows for each description and score under the same category and criterion
            num_lines = max(len(descriptions), len(scores))

            for i in range(num_lines):
                formatted_criteria.append([
                    category if i == 0 else "",  # Show category in the first row of each group
                    criterion if i == 0 else "",  # Show criterion in the first row of each group
                    details["max_score"] if i == 0 else "",  # Show Max Score only once for each criterion
                    descriptions[i] if i < len(descriptions) else "",  # Description line i
                    scores[i] if i < len(scores) else "",  # Score line i
                ])

    return formatted_criteria

def load_criterias():

    # loading the scoring scheme
    with open(f"{output_dir}/scoring_scheme.json", "r") as json_file:
        scoring_scheme = json.load(json_file)  # Parse the JSON content into a Python dictionary

    criterias = load_nested_criterias(scoring_scheme)
    return criterias

def update_categories(new_weights):
    weights_json = new_weights.to_dict(orient="records")
    new_weights_dict = {item["Category"]: float(item["Importance (%)"]) for item in weights_json if item["Category"] != "" or item["Importance (%)"] != ""}
    total_weight = sum(new_weights_dict.values())

    if total_weight != 100:
        return gr.Textbox(value=f"Error: The total weight must be equal to 100. Current total: {total_weight}", elem_classes="error-message"), new_weights, gr.update(visible=True), False
    
    # updating the scoring scheme
    with open(f"{output_dir}/scoring_scheme.json", "r") as json_file:
        scheme = json.load(json_file)  # Parse the JSON content into a Python dictionary
    
    scheme['weights'] = new_weights_dict

    with open(f"{output_dir}/scoring_scheme.json", "w") as json_file:
        json.dump(scheme, json_file, indent=4)

    updated_weights = [[category, weight] for category, weight in new_weights_dict.items()]
    return gr.Textbox(value="Weights Updated Successfully!"), updated_weights, gr.update(visible=False), True

def convert_to_nested_format(data):
    formatted_criteria = {"criteria": {}}

    # Variables to track the current category and criterion
    current_category = None
    current_criterion = None

    for row in data:
        description = row['Description']

        if not description:  # Skip rows without a valid description
            continue

        category = row['Category']
        criterion = row['Criteria']
        max_score = row['Max Score']
        score = row['Score']

        # Update current_category and current_criterion when a valid value is found
        if category:
            current_category = category
        if criterion:
            current_criterion = criterion

        # Initialize the category and criterion if they don't exist
        if current_category not in formatted_criteria["criteria"]:
            formatted_criteria["criteria"][current_category] = {}
        if current_criterion not in formatted_criteria["criteria"][current_category]:
            formatted_criteria["criteria"][current_category][current_criterion] = {
                'max_score': float(max_score) if max_score else 0,  # Convert to float
                'scoring': {}
            }

        # Add the description and score to the scoring dictionary
        formatted_criteria["criteria"][current_category][current_criterion]['scoring'][description] = float(score) if score else 0  # Convert to float

    return formatted_criteria

def update_criterias(new_criterias):
    criterias_json = new_criterias.to_dict(orient="records")
    new_criteras_dict = convert_to_nested_format(criterias_json)

    # Validation check: Ensure max_score >= max(score) in each criterion
    for category, criteria in new_criteras_dict["criteria"].items():
        for criterion, details in criteria.items():
            criterion_max_score = details['max_score']
            if not criterion_max_score:
                continue  # Skip if no max_score is defined
            
            # Convert all scores in the scoring dictionary to float for comparison
            description_scores = [float(value) for value in details['scoring'].values()]

            max_description_score = max(description_scores, default=0)
            
            # Check and log a warning if criterion max_score is less than the max description score
            if float(criterion_max_score) < max_description_score:
                return gr.Textbox(value=f"Error: Max Score cannot be less than the defined scoring scheme", elem_classes="error-message"), new_criterias, gr.update(visible=True), False

    # updating the scoring scheme
    with open(f"{output_dir}/scoring_scheme.json", "r") as json_file:
        scheme = json.load(json_file)  # Parse the JSON content into a Python dictionary
    
    scheme['criteria'] = new_criteras_dict['criteria']

    with open(f"{output_dir}/scoring_scheme.json", "w") as json_file:
        json.dump(scheme, json_file, indent=4)

    updated_criterias = load_nested_criterias(new_criteras_dict)    
    return gr.Textbox(value="Criterias Updated Successfully!"), updated_criterias, gr.update(visible=False), True

def update_scoring_scheme(new_weights, new_criterias):

    # updating the categories and criterias
    weights_text, weights, weights_visibility, success_flag_w = update_categories(new_weights)
    criterias_text, criterias, criterias_visibility, success_flag_c = update_criterias(new_criterias)

    # Extract category names from weights
    category_names = {category[0] for category in weights}

    # Extract categories present in the criterias
    criterias_categories = {criteria[0] for criteria in criterias if criteria[0]}

    # Find missing categories
    missing_categories = category_names - criterias_categories

    # If any category in weights does not have a corresponding scoring scheme, return an error
    if missing_categories:
        return weights_text, weights, weights_visibility, gr.Textbox(value=f"Error: Add Scoring Criterias for the following Categories: {', '.join(missing_categories)}", elem_classes="error-message"), criterias, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
    
    # incase of logical error:
    if not success_flag_w or not success_flag_c:
        return weights_text, weights, weights_visibility, criterias_text, criterias, criterias_visibility, gr.update(visible=True), gr.update(visible=True), gr.update(visible=True), gr.update(visible=True)
    
    else:
        return weights_text, weights, weights_visibility, criterias_text, criterias, criterias_visibility, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
