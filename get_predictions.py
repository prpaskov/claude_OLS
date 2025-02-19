# Initialize Claude API
claude = ClaudeAPI()

# Read Hackenburg et al. dataset
ssl._create_default_https_context = ssl._create_unverified_context
url = "https://raw.githubusercontent.com/kobihackenburg/scaling-LLM-persuasion/main/main_study/code/analysis/final_data_with_metrics.csv"
response = requests.get(url, verify=False)
df = pd.read_csv(pd.io.common.StringIO(response.text))

# Create the new column for Claude prompt
df['claude_prompt'] = df.apply(claude.create_prompt, axis=1, demo_cols = False, hackenburg_cols = True)

# Take random sample from df, create column for Claude predictions
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
