import pandas as pd
import openai
import os
    
openai.api_key = os.getenv('OPENAI_API_KEY')
df = pd.read_csv('web/data/main.csv')
keywords = []
for index, row in df.iterrows():
    title = row['title']
    prompt = f"Extract 4 separate single words which are most important in the given title which are not small words in \"{title}\”, make every keyword’s first letter upper case.”
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    prompt_result = response.choices[0].message.content.strip()
    keywords.append(prompt_result)

df['keywords'] = keywords        
df.to_csv('web/data/main.csv', index=False)
print(keywords)
