# -*- coding: utf-8 -*-
# Core Pkgs
import streamlit as st 
import pandas as pd

# Data Viz Pkgs
import plotly.express as px 
import altair as alt


# DB Mgmt
from app_utils import view_all_users
from app_utils import view_all_page_visited_details,loggedin_user_activity
import time 
timestr = time.strftime("%Y%m%d-%H%M%S")


def MetricsPage():
	with st.expander("User Profiles"):
		user_result = view_all_users()
		clean_df = pd.DataFrame(user_result)
		st.dataframe(clean_df)

	with st.expander("User Activities"):
		user_activity_results = loggedin_user_activity()
		activity_df = pd.DataFrame(user_activity_results)
		
		activity_df.columns = ['logged_in_email','jobTitle','language','postDetails','postDate','firstname','lastname','email','password','school','year','classlevel','emphasis']
		st.dataframe(activity_df)
		filename_to_save_as = 'useractivities_{}.csv'.format(timestr)
		st.download_button(label='Download User Activities',data=activity_df.to_csv(),file_name=filename_to_save_as,mime='text/csv')

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




