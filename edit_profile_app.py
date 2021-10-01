# -*- coding: utf-8 -*-
# Core Pkgs
import streamlit as st 
import pandas as pd


# DB Mgmt
from app_utils import view_all_users,view_all_user_profiles,get_profile,edit_user_profile_data



def ProfilePage(logged_in_email):
	userprofile_result = get_profile(logged_in_email)
	with st.expander("Current User Profile"):
		userprofile_result_df = pd.DataFrame(userprofile_result)
		st.dataframe(userprofile_result_df)
		

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


		with st.expander("Updated User Profile"):
			# user_result = view_all_users()
			current_user_profile_result = get_profile(logged_in_email) 
			userprofile_df = pd.DataFrame(current_user_profile_result)
			userprofile_df.columns = ['firstname','lastname','email','password','school','year','classlevel','emphasis']
			st.dataframe(userprofile_df)



			
