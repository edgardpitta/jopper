# -*- coding: utf-8 -*-
# Core Pkgs
import streamlit as st 
import pandas as pd

# Data Viz Pkgs
import plotly.express as px 
import altair as alt


# DB Mgmt
from app_utils import view_all_users,view_all_user_profiles,get_profile
from app_utils import view_all_page_visited_details,loggedin_user_activity


def MetricsPage():
	with st.expander("User Profiles"):
		user_result = view_all_users()
		clean_df = pd.DataFrame(user_result)
		# clean_df.columns = ['firstname','lastname','email','password','school','year','classlevel','emphasis']
		st.dataframe(clean_df)

	with st.expander("User Activities"):
		user_activity_results = loggedin_user_activity()
		activity_df = pd.DataFrame(user_activity_results)
		
		activity_df.columns = ['logged_in_email','jobTitle','language','postDetails','postDate','firstname','lastname','email','password','school','year','classlevel','emphasis']
		st.dataframe(activity_df)

	# Page Visited Section
	with st.expander("Page Metrics"):
		page_visited_details = pd.DataFrame(view_all_page_visited_details(),columns=["Pagename","Time_of_Visit"])
		st.dataframe(page_visited_details)

		

	with st.expander("Page Metrics Plots"):
		pg_counts = page_visited_details['Pagename'].value_counts().rename_axis('Pagename').reset_index(name='Counts')
		# st.dataframe(pg_counts)
		# Bar Chart
		c = alt.Chart(pg_counts).mark_bar().encode(x='Pagename',y='Counts',color='Pagename')
		st.altair_chart(c,use_container_width=True)
		# Pie Chart

		p = px.pie(pg_counts,values='Counts',names='Pagename')
		st.plotly_chart(p,use_container_width=True)



def EditAllProfiles_Page():
	with st.expander("User Profiles"):
		user_result = view_all_users()
		clean_df = pd.DataFrame(user_result)
		st.dataframe(clean_df)

	# List all users in database to allow selection
	list_of_users = [i[0] for i in view_all_user_profiles()]
	selected_profile = st.selectbox("User Profiles",list_of_users)
	userprofile_result = get_profile(selected_profile)
	# st.write(userprofile_result)

	if userprofile_result:
		firstname = userprofile_result[0][0]
		lastname = userprofile_result[0][1]
		email = userprofile_result[0][2]
		password = userprofile_result[0][3]
		school = userprofile_result[0][4]
		year = userprofile_result[0][5]
		class_level = userprofile_result[0][6]
		emphasis = userprofile_result[0][7]

		signup_col1,signup_col2 = st.columns(2)
		with signup_col1:
			new_firstname = st.text_input("First Name",firstname)
			new_lastname = st.text_input("Last Name",lastname)
			new_email = st.text_input("Email",email)
			new_password = st.text_input("Password",password,type='password')

		with signup_col2:
			new_school = st.selectbox(school,["School1","School2"])
			new_year = st.text_input("Year",year)
			new_class_level = st.selectbox("Class:{}".format(class_level),["1","2","3"])
			new_emphasis = st.selectbox("Emphasis:{}".format(emphasis),["One","Two"])


		if st.button("Update Profile"):
			edit_user_profile_data(new_firstname,new_lastname,new_email,new_password,new_school,new_year,new_class_level,new_emphasis,firstname,lastname,email,password,school,year,class_level,emphasis)
			st.success("Updated:{} to {}".format(firstname,new_firstname))


		with st.expander("Updated User Profiles"):
			# user_result = view_all_users()
			current_user_profile_result = get_profile(selected_profile) 
			userprofile_df = pd.DataFrame(current_user_profile_result)
			userprofile_df.columns = ['firstname','lastname','email','password','school','year','classlevel','emphasis']
			st.dataframe(userprofile_df)

