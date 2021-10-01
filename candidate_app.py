import streamlit as st
import pandas as pd 
import pdfplumber
import docx2txt
import neattext.functions as nfx
from collections import Counter
# Text Viz Pkgs
from wordcloud import WordCloud 
from textblob import TextBlob
from datetime import datetime


# Data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
import altair as alt 
import seaborn as sns

# DB Mgt
from app_utils import create_uploaded_files_table,add_file_details,create_candidates_table,add_candidates_details,view_all_candidates_details_data,create_page_visited_table,add_page_visited_details,view_all_page_visited_details

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


def get_most_common_tokens_as_df(docx):
	word_freq = Counter(docx.split())
	most_common_tokens = dict(word_freq)
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








def CandidatesPage2():
	create_candidates_table()
	create_uploaded_files_table()
	# Layout
	col1,col2 = st.columns([1,2])

	# Column 1 Layout for jobtitle and language
	with col1:
		job_title = st.text_input("Candidate Profile")
		language_type = st.selectbox("Language",['en','fr','pt'])
		plain_text = st.text_area("Text",height=200)

	# Column 2 Layout for file uploads
	with col2:
		docx_file = st.file_uploader("Upload File",type=['txt','pdf'])
	

	if st.button("Process"):
		
		if docx_file is not None:
			file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
			st.write(file_details)
			# Check File Type
			if docx_file.type == "text/plain":
				raw_text = str(docx_file.read(),"utf-8") # works with st.text and st.write,used for further processing
			elif docx_file.type == "application/pdf":
				try:
					with pdfplumber.open(docx_file) as pdf:
						page = pdf.pages[0]
						raw_text = page.extract_text()
						# st.write(raw_text)
				except:
					st.write("None")

			with st.expander("Original Text"):
				st.text("Text Length:{}".format(len(raw_text)))
				st.write(raw_text)

			# Save Data
			add_candidates_details(job_title,language_type,raw_text,datetime.now())
			add_file_details(docx_file.name,docx_file.type,docx_file.size,datetime.now())
			st.success("Saved Results to DB")
			nlpiffy_text(raw_text)
						    		

		elif plain_text is not None:
			raw_text = plain_text
			with st.expander("Original Text"):
				st.text("Text Length:{}".format(len(raw_text)))
				st.write(raw_text)
			# Save Data
			add_candidates_details(job_title,language_type,raw_text,datetime.now())
			st.success("Saved Results to DB")
			nlpiffy_text(raw_text)


			
def CandidatesPage(email):
	create_candidates_table()
	create_uploaded_files_table()
	# Layout
	col1,col2 = st.columns([1,2])

	# Column 1 Layout for jobtitle and language
	with col1:
		job_title = st.text_input("Candidate Profile")
		language_type = st.selectbox("Language",['en','fr','pt'])
		plain_text = st.text_area("Text",height=200)

	# Column 2 Layout for file uploads
	with col2:
		docx_file = st.file_uploader("Upload File",type=['txt','pdf'])
	

	if st.button("Process"):
		
		if docx_file is not None:
			file_details = {"Filename":docx_file.name,"FileType":docx_file.type,"FileSize":docx_file.size}
			st.write(file_details)
			# Check File Type
			if docx_file.type == "text/plain":
				raw_text = str(docx_file.read(),"utf-8") # works with st.text and st.write,used for further processing
			elif docx_file.type == "application/pdf":
				try:
					with pdfplumber.open(docx_file) as pdf:
						page = pdf.pages[0]
						raw_text = page.extract_text()
						# st.write(raw_text)
				except:
					st.write("None")

			with st.expander("Original Text"):
				st.text("Text Length:{}".format(len(raw_text)))
				st.write(raw_text)

			# Save Data
			add_candidates_details(email,job_title,language_type,raw_text,datetime.now())
			add_file_details(docx_file.name,docx_file.type,docx_file.size,datetime.now())
			st.success("Saved Results to DB")
			nlpiffy_text(raw_text)
						    		

		elif plain_text is not None:
			raw_text = plain_text
			with st.expander("Original Text"):
				st.text("Text Length:{}".format(len(raw_text)))
				st.write(raw_text)
			# Save Data
			add_candidates_details(email,job_title,language_type,raw_text,datetime.now())
			st.success("Saved Results to DB")
			nlpiffy_text(raw_text)

	