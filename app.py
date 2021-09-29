#Core Pkgs
import streamlit as st

# NLP
import neattext as nfx
import spacy
from collections import Counter
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
from textblob import TextBlob
import textdistance as td
from sklearn.feature_extraction.text import TfidfVectorizer

# EDA
import pandas as pd

# Text Downloader
import base64
import time
timestr = time.strftime('%Y%m%d-%H%M%S')


# Data Viz Pkgs
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from wordcloud import WordCloud


# Fxns
def text_analyzer(my_text):
	docx = nlp(my_text)
	allData = [(token.text, token.shape_, token.pos_, token.tag_, token.lemma_,token.is_alpha, token.is_stop) for token in docx]
	df = pd.DataFrame(allData, columns=['Token', 'Shape', 'PoS', 'Tag', 'Lemma', 'IsAlpha', 'IsStopWords'])
	return df

def text_cleaner(my_text):
	docx = nfx(my_text)
	docx = docx.lower().remove_stopwords().remove_numbers().remove_punctuations().remove_special_characters()
	return docx

def plot_wordcloud(my_text):
	my_wordcloud = WordCloud().generate(my_text)
	fig = plt.figure()
	plt.imshow(my_wordcloud, interpolation='bilinear')
	plt.axis('off')
	st.pyplot(fig)

def get_entitities(my_text):
	docx = nlp(my_text)
	entities = [(entity.text, entity.label_) for entity in docx.ents]
	df_entities = pd.DataFrame(entities, columns=['Token', 'Label'])
	return df_entities

def text_downloader(raw_text):
	b64 = base64.b64encode(raw_text.encode()).decode()
	new_filename = "new_text_file_{}_.txt".format(timestr)
	st.markdown("#### Download File ###")
	href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'
	st.markdown(href,unsafe_allow_html=True)

def match(raw_text, job_text):
    j = td.jaccard.similarity(raw_text, job_text)
    s = td.sorensen_dice.similarity(raw_text, job_text)
    c = td.cosine.similarity(raw_text, job_text)
    o = td.overlap.normalized_similarity(raw_text, job_text)
    total = (j+s+c+o)/4
    # total = (s+o)/2
    return total*100

vectorizer = TfidfVectorizer()
def cosine_sim(text1, text2):
	tfidf = vectorizer.fit_transform([text1, text2])
	return ((tfidf * tfidf.T).A)[0,1]

def main():
	st.title('Candidate/Job Posting Matcher')
	
	st.subheader('Job Posting Analysis')

	text_file = st.file_uploader('Upload Txt File', type=['txt'])
	if text_file is not None:
		file_details = {'Filename':text_file.name, 'Filesize':text_file.size, 'Filetype':text_file.type}
		st.write(file_details)
		# Decode Text
		job_text = text_file.read().decode('utf-8')
		st.write(job_text)

		with st.expander('Text Analysis'):
			token_result_df = text_analyzer(job_text)
			st.dataframe(token_result_df)

		st.subheader('Most Common Words in the Job Posting')
		# all tokens that arent stop words or punctuations
		docj = nlp(job_text)
		words = [token.lemma_
		for token in docj
		if not token.is_stop and not token.is_punct]

		# noun tokens that arent stop words or punctuations
		nouns_j = [token.lemma_
			 for token in docj
			 if (not token.is_stop and
			     not token.is_punct and
			     token.pos_ == "NOUN")]


		# ten most common noun tokens
		noun_freq = Counter(nouns_j)
		common_nouns_j = noun_freq.most_common(100)
		df_common_noums_j = pd.DataFrame(common_nouns_j, columns=['Word', 'Ocorrencies'])
		st.dataframe(df_common_noums_j)

		st.subheader('Job Posting Wordcloud')
		plot_wordcloud(job_text)

		st.subheader('Candidate Analysis')
		normalize_case = st.sidebar.checkbox("Normalize Case")
		clean_stopwords = st.sidebar.checkbox('Stopwords')
		clean_punctuations = st.sidebar.checkbox('Puntuations')
		clean_emails = st.sidebar.checkbox('Emails')
		clean_special_char = st.sidebar.checkbox('Special Characters')
		clean_numbers = st.sidebar.checkbox('Numbers')
		clean_urls = st.sidebar.checkbox('URLs')

		raw_text = st.text_area("Enter Text",)
		if st.button("Analyze"):
			col1, col2 = st.columns(2)

			with col1:
				with st.expander('Original Text'):
					st.write(raw_text)
					st.write(dir(nfx))
					text_downloader(raw_text)

			with col2:
				with st.expander('Processed Text'):
					if normalize_case:
							raw_text = raw_text.lower()

					if clean_stopwords:
						raw_text = nfx.remove_stopwords(raw_text)

					if clean_numbers:
						raw_text = nfx.remove_numbers(raw_text)

					if clean_urls:
						raw_text = nfx.remove_urls(raw_text)

					if clean_emails:
						raw_text = nfx.remove_emails(raw_text)

					if clean_punctuations:
						raw_text = nfx.remove_punctuations(raw_text)

					if clean_special_char:
						raw_text = nfx.remove_special_characters(raw_text)

					st.write(raw_text)

			with st.expander('Text Analysis'):
				token_result_df = text_analyzer(raw_text)
				st.dataframe(token_result_df)

			st.subheader('Most Common Noums in Candidate')
			# all tokens that arent stop words or punctuations
			docx = nlp(raw_text)
			words = [token.lemma_
			for token in docx
			if not token.is_stop and not token.is_punct]

			# noun tokens that arent stop words or punctuations
			nouns = [token.lemma_
			         for token in docx
			         if (not token.is_stop and
			             not token.is_punct and
			             token.pos_ == "NOUN")]


			# ten most common noun tokens
			noun_freq = Counter(nouns)
			common_nouns = noun_freq.most_common(100)
			df_common_noums = pd.DataFrame(common_nouns, columns=['Word', 'Ocorrencies'])
			st.dataframe(df_common_noums)


			st.subheader('Candidate Wordcloud')
			plot_wordcloud(raw_text)

			# with st.expander('Plot Wordcloud'):
			# 	plot_wordcloud(token_result_df['Lemma'])

			st.subheader('Parts of Speech (PoS) Tags')
			fig = plt.figure()
			sns.countplot(token_result_df['PoS'])
			plt.xticks(rotation=45)
			st.pyplot(fig)

			st.subheader("Sentiment Analysis")
			blob = TextBlob(raw_text)
			result_sentiment = blob.sentiment
			st.success(result_sentiment)
			st.write('The polarity defines the phase of emotions expressed in the analyzed sentence. It ranges from -1 to 1 and goes like this: Very Positive, Positive, Neutral, Negative, Very Negative')
			st.write('Subjectivity helps in determining the personal states of the speaker including Emotions, Beliefs, and opinions. It has values from 0 to 1 and a value closer to 0 shows the sentence is objective and vice versa.')


			st.subheader('Compared Wordclouds Candidate - Job Posting')
			col1, col2 = st.columns(2)

			with col1:
				st.write('Candidate')
				plot_wordcloud(raw_text)

			with col2:
				st.write('Job Posting')
				plot_wordcloud(job_text)

			st.subheader('Compared Key-words')
			col1, col2 = st.columns(2)

			with col1:
				st.write('Candidate')
				st.dataframe(df_common_noums)

			with col2:
				st.write('Job Posting')
				st.dataframe(df_common_noums_j)

			#st.subheader('Index of Similarity between Job Posting and Candidate')
			#similarity=match(raw_text, job_text)
			#st.write(similarity)
			
			st.subheader('Similarity Index Job Posting and Candidate')
			sim_score = cosine_sim(raw_text, job_text)
			st.write("Jobs vs Candidate:{}".format(sim_score))
			st.write("The percentage of overlap between the candidate's competencies and the job posting requirements.")
    
if __name__ == '__main__':
	main()