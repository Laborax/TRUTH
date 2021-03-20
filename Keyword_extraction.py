def keyword_extraction(link):
    from scrape import c
    test = c(link)
    import nltk.tokenize as nt
    import nltk
    nltk.data.path.append('./nltk_data/')
    text=test[1]
    ss=nt.sent_tokenize(text)
    tokenized_sent=[nt.word_tokenize(sent) for sent in ss]
    pos_sentences=[nltk.pos_tag(sent) for sent in tokenized_sent ]
    i = 0 
    l =[]
    it = iter(range(len(pos_sentences[0])-1))
    for i in it:
        if(pos_sentences[0][i][1] == pos_sentences[0][i+1][1] ):
            l.append([pos_sentences[0][i][0] +' '+ pos_sentences[0][i+1][0],pos_sentences[0][i][1]])
            i=next(it)
        else:
            l.append([pos_sentences[0][i][0] ,pos_sentences[0][i][1]])
    nouns = [word.lower() for (word,pos) in l if(pos=="NNP")]
    words = [sent.lower() for (sent,pos) in l if(pos!="NNP")]   
    words = ' '.join(words)

    def sort_score(matrix):
            tuples = zip(matrix.col, matrix.data)
            return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)  

    def extract_topn_from_vector(feature_names, sorted_items, topn=3):
            sorted_items = sorted_items[:topn]
            score_vals = []
            feature_vals = []

            for idx, score in sorted_items:
                fname = feature_names[idx]
                score_vals.append(round(score, 3))
                feature_vals.append(feature_names[idx])

            results= {}
            for idx in range(len(feature_vals)):
                results[feature_vals[idx]]=score_vals[idx]
            return results

    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english') 
    tfidf_train = tfidf_vectorizer.fit_transform([test[0]])

    feature_names = tfidf_vectorizer.get_feature_names()
    tf_idf_vector = tfidf_vectorizer.transform([words])
    sorted_items=sort_score(tf_idf_vector.tocoo())
    keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    result =[]
    for k in keywords:
        result.append(k)
    
    return nouns+result



#print(keyword_extraction("https://www.indiatoday.in/cities/bengaluru/story/zomato-delivery-executive-allegation-bengaluru-woman-1778362-2021-03-12"))
