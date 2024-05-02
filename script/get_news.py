import newsapi
import requests
import pandas as pd
import random
import csv
from datetime import datetime, timedelta
import os

api_key = os.getenv('NEWSAPI_API_KEY')

def get_news_headlines(domains='bbc.co.uk, bbc.com, nytimes.com, cnn.com, dailymail.co.uk, theguardian.com, foxnews.com, indiatimes.com, people.com, timesofindia.com, usatoday.com,thesun.co.uk, the-sun.com, nypost.com, washingtonpost.com, ndtv.com, cnbc.com, apnews.com', 
                      language='en', 
                      from_param=(datetime.now()- timedelta(hours = 24)).strftime('%Y-%m-%d'+'T00:00:00'),  
                      to_param=datetime.now().strftime('%Y-%m-%d'+'T06:59:00'),
                      sort_by='publishAt',
                      page_size=100,
                      api_key=api_key
                      ):
    api_query = f'https://newsapi.org/v2/everything?domains={domains}&language={language}&from={from_param}&to={to_param}&sortBy={sort_by}&pageSize={page_size}&apiKey={api_key}'

    response = requests.get(api_query)
    
    if response.status_code == 200:
        data_return = response.json()
        data_return['articles'] = list(data_return['articles'])
        
        total_results = data_return.get('totalResults', 0)
        print(f"Total results: {total_results}")

        # Clean title's char
        clean_articles = []
        special_chars = '-!@#$%^&*()_+{}[]|\\:;"\'<>,.?/~`'
        
        for i in data_return['articles']:
            title = i['title']
            if not any(char in title for char in special_chars) and title.isascii():
                clean_articles.append(i)
        print(f"Total results after chars cleaning: {len(clean_articles)}")
        
        # Filter out titles with less than 5 words
        qualified_articles = []
        for x in clean_articles:
            title = x['title']
            words = title.split()
            if len(words) >= 5:
                qualified_articles.append(x)
        print(f"Total results after filtering: {len(qualified_articles)}")
        
        # Select four random articles
        four_random_articles = random.sample(qualified_articles, 4)

        return four_random_articles

game_articles = get_news_headlines()
#print(game_articles)
csv_filename = 'web/data/main.csv'


def write_game_articles_to_csv(game_articles, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        column_names = ['group_id', 'title', 'published_at', 'url', 'keywords']
        writer = csv.DictWriter(csvfile, fieldnames=column_names)

        writer.writeheader()

        group_ids = [1, 2, 3, 4]
        for i, article in enumerate(game_articles):
            writer.writerow({
                'group_id': group_ids[i],
                'title': article['title'],
                'published_at': article['publishedAt'],
                'url': article['url']
            })
    
    with open(csv_filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

write_game_articles_to_csv(game_articles, csv_filename)
