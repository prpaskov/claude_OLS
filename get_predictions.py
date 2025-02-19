import time
import pandas as pd
import requests

# Initialize Claude API
from claude_predict import ClaudePredict
claude = ClaudePredict()

 # Set survey questions, using only survey question 1 (of 4) from https://github.com/kobihackenburg/scaling-LLM-persuasion/blob/main/SI_Appendix.pdf
SURVEY_QUESTIONS = {
    'medicaid': "The U.S. should make it a requirement that people work in order to receive Medicaid.",
    'veteran healthcare': "The U.S. should increase privatization of veterans' healthcare.",
    'worker_pensions': "The U.S. should transition pension plans for public workers into privately managed accounts.",
    'foreign_aid': "The U.S. should not decrease foreign aid spending.",
    'solitary_confinement': "The U.S. should not ban the use of solitary confinement for juveniles in prison.",
    'assisted_suicide': "The U.S. should allow terminally ill patients to end their lives via assisted suicide.",
    'border_restrictions': "The U.S. should adopt more restrictions at the U.S. border.",
    'felons_voting': "The U.S. should not deny convicted felons the right to vote.",
    'affirmative_action': "The U.S. should not allow the use of affirmative action programs.",
    'electoral_college': "The U.S. should abolish the electoral college.",
}

# Read Hackenburg et al. dataset
ssl._create_default_https_context = ssl._create_unverified_context
url = "https://raw.githubusercontent.com/kobihackenburg/scaling-LLM-persuasion/main/main_study/code/analysis/final_data_with_metrics.csv"
response = requests.get(url, verify=False)
df = pd.read_csv(pd.io.common.StringIO(response.text))

# Create the new column for Claude prompt
df['claude_prompt'] = df.apply(claude.create_prompt, axis=1, demo_cols = False, hackenburg_cols = True)

# Take random sample from df, create column for Claude predictions. 300 arbitrarily chosen for a pilot; future research may consider power calcs. 
sample_size = 300
df_sample = df.sample(n=sample_size, random_state=48)  
df['claude_preds'] = None

# Process prompts and retrieve prediction
system_prompt = "You are role playing an individual in the U.S. based on the demographics provided to you."
count = 1
for idx, row in df_sample.iterrows():
    print(f'Running prompt {count}/{sample_size}')
    # Get response from Claude
    response = claude.send_prompt(row['claude_prompt'], system_prompt)
    df.at[idx, 'claude_preds'] = claude.extract_number(response['content'])
    count += 1

# Save identifiers and predictions to new dataset
output_df = df[['prolific_id', 'ResponseId', 'claude_prompt', 'claude_preds']]
output_df['prolific_id'] = output_df['prolific_id'].apply(str)
output_df.to_csv('df_claude_preds.csv', index=False)
