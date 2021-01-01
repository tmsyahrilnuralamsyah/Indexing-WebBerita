from bs4 import BeautifulSoup
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from string import punctuation
import os

kompas_dir = os.listdir('download/')
# print(kompas_dir)

get_stemmer = StemmerFactory()
stemmer = get_stemmer.create_stemmer()

get_stopword = StopWordRemoverFactory()
# more_stopword = ['viva', 'tes']
# data = get_stopword.get_stop_words()+more_stopword
stopword = get_stopword.create_stop_word_remover()

def clean_text(text_data):
    content = text_data
    content = content.translate(str.maketrans('', '', punctuation))
    content = stopword.remove(content)
    words = stemmer.stem(content.lower())
    return words

for art in kompas_dir:
    art_number = art.split('.')[0].split('-')[1]
    print('Cleaning file Kompas-{}.html'.format(art_number))
    raw = BeautifulSoup(open('download/Kompas-'+ art_number +'.html', encoding='utf8'), 'html.parser')

    title = raw.find('title').get_text()
    url = raw.find('meta', {'property': 'og:url'}).attrs['content']
    try:
        contents = raw.find('div', {'class': 'read__content'}).find_all('p')
    except:
        continue

    article = []
    for content in contents:
        for news in content.find_all('strong'):
            news.decompose()
        if (content.get_text() == ''):
            continue
        article.append(content.get_text())

    top = int(len(article)*0.2)
    middle = int(len(article)*0.4)
    tags = []
    article_url = '<url>'+ url +'</url>\n\n'
    article_title = '<title>'+ clean_text(str(title)) +'</title>\n\n'
    article_top = ' '.join(article[:top])
    try:
        article_top = '<top>'+ clean_text(article_top.split(' - ')[1]) +'</top>\n\n'
    except IndexError as identifier:
        article_top = '<top>'+ clean_text(article_top) +'</top>\n\n'
    
    article_middle = '<middle>'+ clean_text(' '.join(article[top:middle])) +'</middle>\n\n'
    article_bottom = '<bottom>'+ clean_text(' '.join(article[middle:])) +'</bottom>'

    tags.extend([article_url, article_title, article_top, article_middle, article_bottom])
    file = open('cleaned/Kompas-'+ art_number +'-bersih.html', 'w', encoding='utf8')
    
    for tag in tags:
        file.write(tag)
    file.close