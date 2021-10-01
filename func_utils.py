# Core pkgs
import streamlit as st

# EDA & File Pkgs
import pandas as pd 
import pdfplumber
import docx2txt
import os

# NLP Pkgs & Text Viz Pkgs
import neattext.functions as nfx
from collections import Counter
from wordcloud import WordCloud 
from textblob import TextBlob
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

# Data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
import altair as alt 
import seaborn as sns

TEMP_DIR = 'tempDir'


# NLP:
#     • Convert the pdf file to txt and show it, if it is the case; otherwise use the text provided in the text field
#     • Validate if the candidate material is in the same language of the job posting provided. If not, show an error message.
#     • Text cleaning (remove stopwords, numbers, punctuations, special chars) and tokenization
#     • Create Wordcloud with most common tokens
#     • Create db user_info with token counting
#     • Show table with 20 most common tokens
#     • Show table with the ten most common competencies (match with a list we will create and update)
#     • Show chart with Parts of Speech – PoS tags
#     • Sentiment analysis (polarity and subjectivity)

def preprocess_text(text):
	processed_text = nfx.remove_special_characters(nfx.remove_stopwords(text))
	return processed_text

def tfidf_vectorizer(text):
	pass 

def get_most_common_tokens(docx,num=10):
	word_freq = Counter(docx.split())
	most_common_tokens = word_freq.most_common(num)
	return dict(most_common_tokens)


def get_most_common_tokens_as_df(docx,num=10):
	word_freq = Counter(docx.split())
	d = dict(word_freq.most_common(num))
	most_common_tokens = dict(sorted(d.items(), key=lambda x: x[1]))
	df = pd.DataFrame({'tokens':most_common_tokens.keys(),'count':most_common_tokens.values()})
	return df

def generate_tags_with_textblob(docx):
	tagged_tokens = TextBlob(docx).tags
	tagged_df = pd.DataFrame(tagged_tokens,columns=['token','tags'])
	return tagged_df 


def plot_most_common_tokens(docx,num=10):
	word_freq = Counter(docx.split())
	most_common_tokens = word_freq.most_common(num)
	x,y = zip(*most_common_tokens)
	fig = plt.figure(figsize=(20,10))
	plt.bar(x,y)
	plt.title("Most Common Tokens")
	plt.xticks(rotation=45)
	plt.show()
	st.pyplot(fig)


def plot_wordcloud(docx):
	mywordcloud = WordCloud().generate(docx)
	fig = plt.figure(figsize=(20,10))
	plt.imshow(mywordcloud,interpolation='bilinear')
	plt.axis('off')
	st.pyplot(fig)


def analyze_sentiment(docx):
	blob = TextBlob(docx)
	sentiment_results = {'polarity':blob.sentiment.polarity,'subjectivity':blob.sentiment.subjectivity} 
	return sentiment_results

def analyze_sentiment_to_df(docx):
	blob = TextBlob(docx)
	sentiment_results = {'polarity':blob.sentiment.polarity,'subjectivity':blob.sentiment.subjectivity} 
	sentiment_df = pd.DataFrame(sentiment_results.items()).set_index(0).T
	return sentiment_df


def __get_wordcloud(docx):
    mywordcloud = WordCloud().generate(docx)
    return mywordcloud

def __get_most_common_tokens(docx, num=10):
    clean_docx = nfx.remove_stopwords(docx)
    word_freq = Counter(clean_docx.split())
    most_common_tokens = word_freq.most_common(num)
    x, y = zip(*most_common_tokens)
    return x, y



def nlpiffy_text(raw_text):
	processed_text = preprocess_text(raw_text)

	ncol1,ncol2 = st.columns(2)

	with ncol1:
		with st.expander("Tokens"):
			tokens_df = get_most_common_tokens_as_df(processed_text)
			st.dataframe(tokens_df)

	with ncol2:
		# num_tokens = st.number_input("Number of Tokens",2,100,2) # add to sessionstate on settings
		with st.expander("Most Common Tokens"):
			results_for_tokens = get_most_common_tokens(processed_text)
			st.write(results_for_tokens)



	with st.expander("Plot Token Freq"):
		st.info("Plot For Most Common Tokens")
		most_common_tokens = get_most_common_tokens(processed_text,20)
		# st.write(most_common_tokens)
		tk_df = pd.DataFrame({'tokens':most_common_tokens.keys(),'counts':most_common_tokens.values()})
	
		brush = alt.selection(type='interval', encodings=['x'])
		c = alt.Chart(tk_df).mark_bar().encode(
							    x='tokens',
							    y='counts',
							    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
							    ).add_selection(brush)
							
		st.altair_chart(c,use_container_width=True)

	with st.expander("Plot Wordcloud"):
		st.info("word Cloud")
		plot_wordcloud(processed_text)


	with st.expander("Plot PoS Tags"):
		tagged_df = generate_tags_with_textblob(raw_text)
		fig = plt.figure()
		sns.countplot(x='tags',data=tagged_df)
		plt.xticks(rotation=45)
		st.pyplot(fig)

	with ncol1:
		with st.expander("PoS Tags"):
			st.dataframe(tagged_df)


	with ncol2:
		with st.expander("Sentiment Analysis"):
			res = analyze_sentiment(raw_text)['polarity']
			sentiment = 'Positive:😊' if res > 0 else 'Negative:😞'
			st.write(sentiment)
			st.write(analyze_sentiment(raw_text))



vectorizer = TfidfVectorizer()
def cosine_sim(text1, text2):
	tfidf = vectorizer.fit_transform([text1, text2])
	return ((tfidf * tfidf.T).A)[0,1]



def plot_comparisons(processed_text1,processed_text2,token_num=6,filename='plot_comparisons.png'):
	figsize=(20,10)
	xt, yt = __get_most_common_tokens(processed_text1, num=token_num)
	xs, ys = __get_most_common_tokens(processed_text2, num=token_num)
	jobs_wordcloud = __get_wordcloud(processed_text1)
	candidate_wordcloud = __get_wordcloud(processed_text2)
	fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
	fig.suptitle("Subplots[Vertical]")
	ax1.bar(xt, yt)
	ax1.set_title("Tokens Frequency[Jobs]")
	ax1.tick_params(labelrotation=45)
	ax2.bar(xs, ys,color="orange")
	ax2.set_title("Tokens Frequency[Candidate]")
	ax2.tick_params(labelrotation=45)
	ax3.imshow(jobs_wordcloud, interpolation="bilinear")
	ax3.set_title("Wordcloud[Jobs]")
	ax4.imshow(candidate_wordcloud, interpolation="bilinear")
	ax4.set_title("Wordcloud[Candidate]")
	filepath = os.path.join(TEMP_DIR,filename)
	return fig.savefig(filepath)
