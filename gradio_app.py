import gradio as gr
from utils.gradio_fn import toggle_processing_visibility, scores_visibility_off, scores_visibility_on, rank_visibility_off
from utils.gradio_fn import bulk_rank
from utils.gradio_fn import load_criterias, load_weights, update_scoring_scheme
# Read CSS from an external file
with open("style.css", "r") as f:
    custom_css = f.read()

with gr.Blocks(title="Resume Scoring - DEMO", css=custom_css) as app:
    
    # Add logo at the bottom left
    with gr.Row(scale=1):
        with gr.Column():
            gr.Markdown("<div id='app-title'>📄 Resume Scoring Tool</div>")

        # with gr.Column(scale=1, elem_id="logo-column", min_width=100):
        #     logo = gr.Image(value="./qult.jpeg", container = False, visible=True, elem_id="logo", show_label=False, show_download_button=False, show_fullscreen_button=False)  # Replace with actual logo path

    with gr.Row():
        with gr.Column(scale=1, elem_id="input-section"):  # Add an ID for styling
            job_desc = gr.Textbox(
                label="🔍 Enter Job Description", 
                lines=7, 
                placeholder="Paste the job description here...",
                elem_id="job-desc"
            )

            cv_uploads = gr.File(
                label="📂 Upload CVs", 
                file_count="multiple", 
                file_types=[".pdf", ".docx", ".txt"],
                elem_id="cv-upload"
            )

            # Buttons in the same row
            with gr.Row(elem_id="button-row"):
                submit_btn = gr.Button("📊 Rank Resumes", elem_classes="rank-button")
                scheme_btn = gr.Button("📜 Show Scoring Scheme", elem_classes="scoring-button")
    
    
    loading_message = gr.Markdown(visible=False, container=True, height = 70, elem_classes="loading-message")

    with gr.Row():
        with gr.Column(scale=1):
            weights_table = gr.DataFrame(
                label="Categories", 
                headers=["Category", "Importance (%)"], 
                datatype=["str", "number"], 
                interactive=True, 
                visible=False
            )

            with gr.Row():
                w_status_message = gr.Textbox(label = "status", interactive=False, lines=1, visible=False)
    
    with gr.Row():
        with gr.Column(scale=1):
            cv_results_table = gr.HTML(visible=False)

    with gr.Row():
        with gr.Column(scale=1):
            criterias_table = gr.DataFrame(
                label="Criterias", 
                headers=["Category", "Criteria", "Max Score", "Description", "Score"],  # Add Max Score column
                datatype=["str", "str", "number", "str", "number"],  # Adjust datatype for Max Score
                interactive=True, 
                visible=False
            )

            with gr.Row():
                c_status_message = gr.Textbox(label = "status", interactive=False, lines=1, visible=False)

    # Bottom right buttons
    with gr.Row(elem_id="bottom-right-buttons"):  # Apply flex-end styling
        with gr.Column(scale=0.3, min_width=200):  # Smaller column for buttons
            with gr.Row():
                save_score_btn = gr.Button("Save Changes", elem_classes="action-button save-button", visible=False)
                cancel_score_btn = gr.Button("Cancel", elem_classes="action-button cancel-button", visible=False)

    submit_btn.click(
        fn=toggle_processing_visibility,
        inputs=None,
        outputs=[loading_message, cv_results_table],
    )

    submit_btn.click(
        fn=scores_visibility_off,
        inputs=None,
        outputs=[weights_table, save_score_btn, criterias_table, cancel_score_btn, w_status_message, c_status_message]
    )

    submit_btn.click(
        fn=bulk_rank,
        inputs=[job_desc, cv_uploads],
        outputs=[cv_results_table, loading_message, cv_results_table]
    )

    scheme_btn.click(
        fn=scores_visibility_on,
        inputs=None,
        outputs=[weights_table, save_score_btn, criterias_table, cancel_score_btn]
    )

    scheme_btn.click(
        fn=rank_visibility_off,
        inputs=None,
        outputs=[cv_results_table, loading_message]
    )

    scheme_btn.click(
        fn=load_weights,
        inputs=[],
        outputs=weights_table
    )

    scheme_btn.click(
        fn=load_criterias,
        inputs=[],
        outputs=criterias_table,
    )

    save_score_btn.click(
        fn=update_scoring_scheme,
        inputs=[weights_table, criterias_table],
        outputs=[w_status_message, weights_table, w_status_message, c_status_message, criterias_table, c_status_message, weights_table, save_score_btn, criterias_table, cancel_score_btn],
    )

    cancel_score_btn.click(
        fn=scores_visibility_off,
        inputs=None,
        outputs=[weights_table, save_score_btn, criterias_table, cancel_score_btn, w_status_message, c_status_message]
    )

app.launch()
