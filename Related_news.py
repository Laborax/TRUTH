def find(link):
    import re
    import csv
    from time import sleep
    from bs4 import BeautifulSoup
    import requests
    from Keyword_extraction import keyword_extraction

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.google.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
    }

    def get_article(card):
        """Extract article information from the raw html"""
        headline = card.find('h4', 's-title').text
        source = card.find("span", 's-source').text
        posted = card.find('span', 's-time').text.replace('·', '').strip()
        description = card.find('p', 's-desc').text.strip()
        raw_link = card.find('a').get('href')
        unquoted_link = requests.utils.unquote(raw_link)
        pattern = re.compile(r'RU=(.+)\/RK')
        clean_link = re.search(pattern, unquoted_link).group(1)
        
        article = {"headline":headline,"time": posted,"summary": description,"link": clean_link}
        return article

    def get_the_news(search):
        """Run the main program"""
        template = 'https://news.search.yahoo.com/search?p={}'
        url = template.format(search)
        articles = []
        links = set()
        
        while True:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div', 'NewsArticle')
            
            # extract articles from page
            for card in cards:
                article = get_article(card)
                link = article['link']
                if not link in links:
                    links.add(link)
                    articles.append(article)        
                    
            # find the next page
            try:
                url = soup.find('a', 'next').get('href')
                sleep(1)
            except AttributeError:
                break
        
            

        return articles[:2]

    keywords = keyword_extraction(link)

    articles1 = get_the_news(keywords[0]+' '+keywords[1])
    articels2 = get_the_news(keywords[1]+' '+keywords[2])

    final_article = articles1+ articels2
    # with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(['Headline', 'Source', 'Posted', 'Description', 'Link'])
    #         writer.writerows(final_article)
    return final_article

#rint(find("https://www.indiatoday.in/cities/bengaluru/story/zomato-delivery-executive-allegation-bengaluru-woman-1778362-2021-03-12"))