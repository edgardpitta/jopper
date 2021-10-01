import streamlit as st
import pandas as pd 
# import pdfplumber
# import docx2txt
import neattext.functions as nfx
from collections import Counter
from datetime import datetime
# Text Viz Pkgs
from wordcloud import WordCloud 


# Data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
import altair as alt 

# DM Mgmt
from app_utils import create_uploaded_files_table,add_file_details,view_all_filedetails_data,create_jobposting_table,add_jobposting_details,view_all_jobposting_details_data

# #### 2. Job Posting
# Users upload pdf or txt files with job postings. 

# Fields:
#     • Job_Title – text
#     • Determine Language – en, fr, pt
#     • File upload


# NLP:
#     • Text cleaning (remove stopwords, numbers, punctuations, special chars) and tokenization
#     • TF-IDF analysis
#     • Create db job_posting with token counting
#     • Plot Wordcloud with most common TF-IDF tokens
#     • Show a list of most common words

def preprocess_text(text):
	processed_text = nfx.remove_special_characters(nfx.remove_stopwords(str(text).lower()))
	return processed_text

def tfidf_vectorizer(text):
	pass 

def get_most_common_tokens(docx,num=10):
	word_freq = Counter(docx.split())
	most_common_tokens = word_freq.most_common(num)
	return dict(most_common_tokens)


def get_most_common_tokens_as_df(docx):
	word_freq = Counter(docx.split())
	d = dict(word_freq)
	most_common_tokens = dict(sorted(d.items(), key=lambda x: x[1]))
	df = pd.DataFrame({'tokens':most_common_tokens.keys(),'count':most_common_tokens.values()})
	return df


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




def JobPostingPage(email):
	create_jobposting_table()

	# Layout
	
	with st.form(key='JobPostForm'):
		col1,col2 = st.columns([1,3])

		# Column 1 Layout for jobtitle and language
		with col1:
			job_title = st.text_input("Job Title (required)")
			if not job_title:
				st.warning("Job Title is required")
			language_type = st.selectbox("Language",['en','fr','pt'])

		# Column 2 Layout for file uploads
		with col2:
			raw_text = st.text_area("Text")
			processed_text = preprocess_text(raw_text)

		submit_button = st.form_submit_button(label='Process')


	if submit_button:


		# Save Data
		add_jobposting_details(email,job_title,language_type,raw_text,datetime.now())
		st.success("Saved Results to DB")
		results_col1,results_col2 = st.columns(2)
		with results_col1:
			with st.expander("Tokens"):
				tokens_df = get_most_common_tokens_as_df(processed_text)
				st.dataframe(tokens_df)


			# num_tokens = st.number_input("Number of Tokens",2,100,2) # add to sessionstate on settings
			with st.expander("Most Common Tokens"):
				results_for_tokens = get_most_common_tokens(processed_text)
				st.write(results_for_tokens)


		with results_col2:
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




		

				

	