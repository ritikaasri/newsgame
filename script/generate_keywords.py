import pandas as pd
import openai
import os
from datetime import datetime

# Set up OpenAI API key  
openai.api_key = os.getenv('OPENAI_API_KEY')

df = pd.read_csv('web/data/main.csv')

# Generate keywords and store to keywords
keywords = []
for index, row in df.iterrows():
    title = row['title']
    # prompt = f"Extract 4 separate single word which are most important in \"{title}\". Format: without punctuation, sepatate by comma. If keyword contains '-', take remove '-' in between. "
    prompt = f"From each \"{title}\", extract only 4 separate single word which are most important to the content and not duplicate with keywords extracted from other title, then output the keyword with this format: without punctuation, separate  by comma. "
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    prompt_result = response.choices[0].message.content.strip()
    prompt_result = prompt_result.split(",")
    prompt_result = list(map(lambda x:x.upper(),prompt_result))
    prompt_result = ",".join(prompt_result)
    keywords.append(prompt_result)

# Update main.csv with keywords
df['keywords'] = keywords        
df.to_csv('web/data/main.csv', index=False)
print(keywords)

# Add timestamp column to main.csv for tracing use
df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Save the new lines to history.csv
history_directory = 'history/history.csv'
if os.path.exists(history_directory):
    history_df = pd.read_csv(history_directory)
    history_df = pd.concat([history_df, df[[ 'group_id', 'title', 'published_at', 'url', 'keywords', 'timestamp']]])
else:
    history_df = df[[ 'group_id', 'title', 'published_at', 'url', 'keywords', 'timestamp']]
history_df.to_csv(history_directory, index=False)
