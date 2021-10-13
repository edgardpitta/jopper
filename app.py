# -*- coding: utf-8 -*-
# Core Pkgs
import streamlit as st 
import streamlit.components.v1 as stc 
import pandas as pd
import re
from datetime import datetime


import plotly.express as px 
import altair as alt

# Pages
from jobposting_app import JobPostingPage
from candidate_app import CandidatesPage
from matcher_app import MatcherPage,MatcherPage_For_LoggedIn_Email
from metrics_app import MetricsPage
from reports_app import ReportsPage
from edit_profile_app import ProfilePage
from edit_posting_app import ShowJobPostsPage,ShowCandidatesPostsPage,ShowCandidatesPostsPage_For_LoggedIn_User
from admin_dashboard_app import EditAllProfiles_Page


# DB Mgmt
from app_utils import (create_uploaded_files_table,create_candidates_table,create_page_visited_table,add_page_visited_details,view_all_page_visited_details,create_jobposting_table)
from app_utils import (create_usertable,add_userdata,login_user,view_all_users,login_admin)

EMAIL_REGEX =  re.compile(r"[\w\.-]+@[\w\.-]+")

def validate_email(email):
	if re.match(EMAIL_REGEX, email):
		return email 



def main():
	create_usertable()
	create_jobposting_table()
	create_candidates_table()
	create_uploaded_files_table()
	create_page_visited_table()
	
	menu = ["Home-Login","Signup","Manage","About"]
	choice = st.sidebar.selectbox("Menu",menu)


	# if choice == "Home":
	# 	# Track Page
	# 	add_page_visited_details('Home',datetime.now())
	# 	st.subheader("Job Analyzer Apps")
	# 	# st.write(st.__version__)

	if choice == "Home-Login":
		# Track Page
		add_page_visited_details('Login',datetime.now())
		st.subheader("Login")

		user_email = st.sidebar.text_input("Email")
		# QA: using username or email
		user_password = st.sidebar.text_input("Password",type='password')
		login_button = st.sidebar.checkbox("Log In")

		if login_button:
			access_granted = login_user(user_email,user_password)
			if access_granted:
				st.info("Login as:{}".format(user_email))
				menu_users = ["JobPosting","Candidates","Matcher","Edit Candidates","Edit Profile"]
				user_choice = st.sidebar.selectbox("User Menu",menu_users)
				if user_choice == "JobPosting":
					st.subheader("Job Posting")
					JobPostingPage(user_email)

				elif user_choice == "Candidates":
					st.subheader("Candidates Material")
					CandidatesPage(user_email)


				elif user_choice == "Matcher":
					st.subheader("Matcher")
					MatcherPage_For_LoggedIn_Email(user_email)

				elif user_choice == "Edit Profile":
					st.subheader("Edit Profile")
					ProfilePage(user_email)

				elif user_choice == "Edit Candidates":
					st.subheader("Edit Candidates")
					ShowCandidatesPostsPage_For_LoggedIn_User(user_email)
			else:
				st.warning("Incorrect Email or Password")



	elif choice == "Signup":
		# Track Page
		add_page_visited_details('Signup',datetime.now())
		st.subheader("Signup")

		with st.form(key="SignupForm"):
			signup_col1,signup_col2 = st.columns(2)
			with signup_col1:
				firstname = st.text_input("First Name")
				lastname = st.text_input("Last Name")
				email = st.text_input("Email")
				new_password = st.text_input("Password",type='password')

			with signup_col2:
				school = st.selectbox("School",["Belo Campus","Other"])
				year = st.date_input("Year",)
				class_level = st.selectbox("Class",[1,2,3,4,5,6,7,8,9,10])
				emphasis = st.selectbox("Emphasis",["M1", "CFM", "IB", "PPMBD", "IMBD", "Other"])

			button = st.form_submit_button(label="Signup")
		if button:
			is_email = validate_email(email)
			if is_email is not None:
				st.success("Your account has been created")
				add_userdata(firstname=firstname,lastname=lastname,email=email,password=new_password,
					school=school,year=year,classlevel=class_level,emphasis=emphasis)
			else:
				st.warning("Invalid Email")


	elif choice == "Manage":
		# Track Page
		add_page_visited_details('Manage',datetime.now())
		st.subheader("Admin Login")
		admin_email = st.sidebar.text_input("Email")
		admin_password = st.sidebar.text_input("Password",type='password')
		admin_login_button = st.sidebar.checkbox("Log In")

		if admin_login_button:
			admin_access_granted = login_admin(admin_email,admin_password)
			if admin_access_granted:
				st.success("Hello Admin")
				menu_admin = ["Matcher","Reports","Edit-All-Users","All-Job-Posts","All-Candidates-Posts","AppMetrics"]
				admin_choice = st.sidebar.selectbox("Admin Menu",menu_admin)
				if admin_choice == "Reports":
					st.subheader("Reports")
					ReportsPage()

				elif admin_choice == "Matcher":
					st.subheader("Matcher")
					MatcherPage()

				elif admin_choice == "All-Job-Posts":
					st.subheader("Job Posts")
					ShowJobPostsPage()

				elif admin_choice == "All-Candidates-Posts":
					st.subheader("Candidates Posts")
					ShowCandidatesPostsPage()


				elif admin_choice == "Edit-All-Users":
					st.subheader("Edit All Profiles")
					EditAllProfiles_Page()


				else:
					st.subheader("AppMetrics")
					MetricsPage()
		

	else:
		# Track Page
		add_page_visited_details('About',datetime.now())
		st.subheader("About")


if __name__ == '__main__':
	main()




