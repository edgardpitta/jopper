# -*- coding: utf-8 -*-
# Core Pkgs
import streamlit as st 
import pandas as pd

# Data Viz Pkgs
import plotly.express as px 
import altair as alt


from app_utils import create_usertable,view_all_users,loggedin_user_activity,view_all_candidates_details_data
from func_utils import plot_wordcloud,get_most_common_tokens,get_most_common_tokens_as_df


#     5. Admin Reports (Only admin users can see these reports)
# Create reports aggregated by the fields (alone or combined):
#         a. Campus/School  - dropdown
#         b. Year – date MM-YYYY
#         c. Class – dropdown 
#         d. Specialization
#         e. Job title
# #### Reports:
#     • Show a table/wordcloud with the most common tokens of a certain group of users  according to the parameters above (for instance: all students of the same class, or the same year, or a combination of both)
#     • Plot a graph with the combined sentiment analysis of a certain group of users
#     • Plot a graph with the combined subjectivity analysis of a certain group of users 
#     • Show a table with the matching score of all users of a certain group of users
# - Selection (Select boxes)
# -- School
# -- Year
# -- Class
# -- Emphasis
# -- Job Title (field in Job Posting)
# -- Candidate Profile (field in Candidates)

# Generate the following for the selection above: 
# - Show a wordcloud with the most commom Job Posting tokens 

# - Show a wordcloud with the most commom Candidate tokens 

# - Show a wordcloud with the similar_tokens 

# - Show a wordcloud with the disimilar_tokens 

# - Plot Sentiment Analysis graphs (x=polarity and y=subjectivity) for the selection

# - Show a dataframe with: 
# -- Higher similarity score 
# -- Average similarity score 
# -- Lower similarity score 

def ReportsPage():
	st.subheader("Reports Page")

	
	user_activity_results = loggedin_user_activity()
	activity_df = pd.DataFrame(user_activity_results)
	activity_df.columns = ['logged_in_email','jobTitle','language','postDetails','postDate','firstname','lastname','email','password','school','year','classlevel','emphasis']
	selected_column = st.selectbox("Columns",activity_df.columns.tolist())
	st.info("Showing Results for Groupby:{}".format(selected_column))
	activity_aggregrated_results = activity_df.groupby(selected_column).count()
	activity_groups = activity_df.groupby(selected_column)
	group_list = list(activity_groups.groups.keys())
	
	# st.write(activity_groups.get_group('edgard@gmail.com'))
	# em,frame = next(iter(activity_groups))
	# st.write(em)
	# st.write(frame)

	with st.expander("User Activities"):
		st.dataframe(activity_df)

	with st.expander("Aggregated Counts"):
		st.dataframe(activity_aggregrated_results)


	with st.expander("Aggregated Details"):
		# st.write(activity_groups)
		selected_single_group = st.selectbox("Columns",group_list)
		new_aggregated_df = activity_groups.get_group(selected_single_group)
		st.write(new_aggregated_df)
		all_post_details = ' '.join(new_aggregated_df['postDetails'].tolist())
		grouped_tokens = get_most_common_tokens_as_df(all_post_details)

		gcol1,gcol2 = st.columns(2)

		with gcol1:
			st.info("Most Common Tokens")
			st.write(grouped_tokens)

		with gcol2:
			st.success('Grouped WordCloud')
			plot_wordcloud(all_post_details)



	with st.expander("JobPosting"):
		all_jobpost_details = ' '.join(activity_df['postDetails'].tolist())
		grouped_tokens = get_most_common_tokens_as_df(all_jobpost_details)
		jobcol1,jobcol2 = st.columns([1,2])

		with jobcol1:
			st.info("Most Common Tokens")
			st.write(grouped_tokens)

		with jobcol2:
			st.success('Grouped JobPost WordCloud')
			plot_wordcloud(all_jobpost_details)


	with st.expander("Candidate"):
		all_candidates_results_df = pd.DataFrame(view_all_candidates_details_data())
		# st.write(all_candidates_results_df)
		all_candidates_results_df.columns = ['candidatesEmail','candidatesTitle','language','postDetails','postDate']
		all_candidatespost_details = ' '.join(all_candidates_results_df['postDetails'].tolist())
		grouped_tokens = get_most_common_tokens_as_df(all_candidatespost_details)
		jobcol1,jobcol2 = st.columns([1,2])

		with jobcol1:
			st.info("Most Common Tokens")
			st.write(grouped_tokens)

		with jobcol2:
			st.success('Grouped Candidates WordCloud')
			plot_wordcloud(all_candidatespost_details)















	







