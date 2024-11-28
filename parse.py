from bs4 import BeautifulSoup
import requests as r
from datetime import datetime

def parse(keywords):
  url = 'https://habr.com/ru/articles/'
  response = r.get(url)
  html = response.text

  soup = BeautifulSoup(html, "html.parser")
  articles = soup.select('article.tm-articles-list__item')
  

  interesting = []

  for article in articles:
    article_url = f'https://habr.com{article.select('h2.tm-title')[0].select('a.tm-title__link')[0]['href']}'

    new_soup = BeautifulSoup(r.get(article_url).text, "html.parser")

    title = new_soup.find('h1', class_='tm-title tm-title_h1').select('span')[0].text

    hubs = [hub.select('span') for hub in new_soup.findAll('a', class_='tm-publication-hub__link')]

    tags = [tag.select('span') for tag in new_soup.select('a.tm-tags-list__link')]

    text = '\n'.join([txt.text for txt in new_soup.select('.article-formatted-body')[0].find_all(['p', 'span', 'h2'])]).lower()
    
    for kw in keywords:
      if any([kw in art for art in [title, hubs, tags, text]]):
        date = datetime.strptime(new_soup.select('span.tm-article-datetime-published')[0].find('time')['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d %B %Y, %H:%M:%S")
        if [date, title, article_url] not in interesting:
          interesting.append([date, title, article_url])
    
  return interesting if len(interesting) > 0 else 'Не нашел статьи по твоим интересам'


      