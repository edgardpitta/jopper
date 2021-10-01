# -*- coding: utf-8 -*-
# Core Pkgs
import streamlit as st 
import pandas as pd
from datetime import datetime


# DB Mgmt
from app_utils import (view_all_jobposting_details_data,view_all_jobtitles_for_jobposting,get_post_by_jobtitle,view_all_candidates_details_data,
	view_all_jobtitles_for_candidates,get_candidate_by_jobtitle,edit_candidates_data)
from app_utils import (view_all_jobtitles_for_candidates_for_loggedin_user,view_all_jobtitles_for_jobposting_for_loggedin_user)



def ShowJobPostsPage():
	jobposting_results = view_all_jobposting_details_data()
	with st.expander("All Job Posting"):
		jobposting_result_df = pd.DataFrame(jobposting_results)
		jobposting_result_df.columns = ['email','jobTitle','language','postDetails','postDate']
		st.dataframe(jobposting_result_df)
		

# 1. Make the Candidate Profiles editable (this is the very reason of this app: help students to improve their CVs)
def ShowCandidatesPostsPage():
	all_candidates_results = view_all_candidates_details_data()
	with st.expander("All Candidates Posts"):
		all_candidates_result_df = pd.DataFrame(all_candidates_results )
		all_candidates_result_df.columns = ['candidatesEmail','candidatesTitle','language','postDetails','postDate']
		st.dataframe(all_candidates_result_df)

	candidates_list = [i[0] for i in view_all_jobtitles_for_candidates()]
	choice = st.sidebar.selectbox('Candidate Title',candidates_list)
	selected_candidate = get_candidate_by_jobtitle(choice)
	st.write(selected_candidate)

	if selected_candidate:
		candidatesEmail = selected_candidate[0][0]
		candidatesTitle = selected_candidate[0][1]
		language = selected_candidate[0][2]
		postDetails = selected_candidate[0][3]
		postDate = selected_candidate[0][4]

		col1,col2 = st.columns(2)
		with col1:
			new_candidatesTitle = st.text_input("Candidate Title",candidatesTitle)
			new_language = st.text_input("Language",language)

		with col2:
			new_postDetails = st.text_area("Post Details",postDetails)


		if st.button("Update Candidate Details"):
			new_postDate = datetime.now()
			edit_candidates_data(new_candidatesTitle,new_language,new_postDetails,new_postDate,candidatesTitle,language,postDetails,postDate)
			st.success("Updated:{} to {}".format(postDetails,new_postDetails))


			all_candidates_results = view_all_candidates_details_data()
			with st.expander("Updated Candidates Posts"):
				all_candidates_result_df = pd.DataFrame(all_candidates_results )
				all_candidates_result_df.columns = ['candidatesEmail','candidatesTitle','language','postDetails','postDate']
				st.dataframe(all_candidates_result_df)


def ShowJobPostsPage():
	jobposting_results = view_all_jobposting_details_data()
	with st.expander("All Job Posting"):
		jobposting_result_df = pd.DataFrame(jobposting_results)
		jobposting_result_df.columns = ['email','jobTitle','language','postDetails','postDate']
		st.dataframe(jobposting_result_df)
		

# 1. Make the Candidate Profiles editable (this is the very reason of this app: help students to improve their CVs)
def ShowCandidatesPostsPage_For_LoggedIn_User(email):
	candidates_list = [i[0] for i in view_all_jobtitles_for_candidates_for_loggedin_user(email)]
	choice = st.sidebar.selectbox('Candidate Title',candidates_list)
	selected_candidate = get_candidate_by_jobtitle(choice)
	st.info("You are Editing:{}".format(choice))
	st.write(selected_candidate)

	if selected_candidate:
		candidatesEmail = selected_candidate[0][0]
		candidatesTitle = selected_candidate[0][1]
		language = selected_candidate[0][2]
		postDetails = selected_candidate[0][3]
		postDate = selected_candidate[0][4]

		col1,col2 = st.columns(2)
		with col1:
			new_candidatesTitle = st.text_input("Candidate Title",candidatesTitle)
			new_language = st.text_input("Language",language)

		with col2:
			new_postDetails = st.text_area("Post Details",postDetails)


		if st.button("Update Candidate Details"):
			new_postDate = datetime.now()
			edit_candidates_data(new_candidatesTitle,new_language,new_postDetails,new_postDate,candidatesTitle,language,postDetails,postDate)
			st.success("Updated:{} to {}".format(postDetails,new_postDetails))


			all_candidates_results = get_candidate_by_jobtitle(choice)
			with st.expander("Updated Candidates Posts"):
				all_candidates_result_df = pd.DataFrame(all_candidates_results )
				all_candidates_result_df.columns = ['candidatesEmail','candidatesTitle','language','postDetails','postDate']
				st.dataframe(all_candidates_result_df)







		
			
