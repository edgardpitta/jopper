# Database Mgmt
import sqlite3 
# conn = sqlite3.connect('data.db')
conn = sqlite3.connect('data.db',check_same_thread=False) # Fix ProgrammingError for thread
c = conn.cursor()


# Create Tables For Uploaded Files
def create_uploaded_files_table():
	c.execute('CREATE TABLE IF NOT EXISTS uploadedFilesTable(filename TEXT,filetype TEXT,filesize TEXT,uploadDate TIMESTAMP)')

# Add Details
def add_file_details(filename,filetype,filesize,uploadDate):
	c.execute('INSERT INTO uploadedFilesTable(filename,filetype,filesize,uploadDate) VALUES (?,?,?,?)',(filename,filetype,filetype,uploadDate))
	conn.commit()


# View Details
def view_all_filedetails_data():
	c.execute('SELECT * FROM uploadedFilesTable')
	data = c.fetchall()
	return data


# Storage for User Post Details
# Create Tables For Job Posting
def create_jobposting_table():
	c.execute('CREATE TABLE IF NOT EXISTS jobPostingTable(email TEXT,jobTitle TEXT,language TEXT,postDetails TEXT,postDate TIMESTAMP)')

# Add Details
def add_jobposting_details(email,jobTitle,language,postDetails,postDate):
	c.execute('INSERT INTO jobPostingTable(email,jobTitle,language,postDetails,postDate) VALUES (?,?,?,?,?)',(email,jobTitle,language,postDetails,postDate))
	conn.commit()


# View Details
def view_all_jobposting_details_data():
	c.execute('SELECT * FROM jobPostingTable')
	data = c.fetchall()
	return data


def get_post_by_jobtitle(jobTitle):
	c.execute('SELECT * FROM jobPostingTable WHERE jobTitle="{}"'.format(jobTitle))
	data = c.fetchall()
	return data

def view_all_jobtitles_for_jobposting():
	c.execute('SELECT DISTINCT jobTitle FROM jobPostingTable')
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data

def view_all_jobtitles_for_jobposting_for_loggedin_user(email):
	c.execute('SELECT DISTINCT jobTitle FROM jobPostingTable WHERE email="{}"'.format(email))
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data


# Create Tables For Candidate Material
def create_candidates_table():
	c.execute('CREATE TABLE IF NOT EXISTS candidatesPostingTable(candidatesEmail TEXT,candidatesTitle TEXT,language TEXT,postDetails TEXT,postDate TIMESTAMP)')

# Add Details
def add_candidates_details(candidatesEmail,candidatesTitle,language,postDetails,postDate):
	c.execute('INSERT INTO candidatesPostingTable(candidatesEmail,candidatesTitle,language,postDetails,postDate) VALUES (?,?,?,?,?)',(candidatesEmail,candidatesTitle,language,postDetails,postDate))
	conn.commit()


# View Details
def view_all_candidates_details_data():
	c.execute('SELECT * FROM candidatesPostingTable')
	data = c.fetchall()
	return data

def get_candidate_by_jobtitle(candidatesTitle):
	c.execute('SELECT * FROM candidatesPostingTable WHERE candidatesTitle="{}"'.format(candidatesTitle))
	data = c.fetchall()
	return data

def view_all_jobtitles_for_candidates():
	c.execute('SELECT DISTINCT candidatesTitle FROM candidatesPostingTable')
	data = c.fetchall()
	# for row in data:
	# 	print(row)
	return data

def view_all_jobtitles_for_candidates_for_loggedin_user(candidatesEmail):
	c.execute('SELECT DISTINCT candidatesTitle FROM candidatesPostingTable WHERE candidatesEmail="{}"'.format(candidatesEmail))
	data = c.fetchall()
	return data


def edit_candidates_data(new_candidatesTitle,new_language,new_postDetails,new_postDate,candidatesTitle,language,postDetails,postDate):
	c.execute("UPDATE candidatesPostingTable SET candidatesTitle =?,language=?, postDetails=?,postDate=? WHERE  candidatesTitle=? and language=? and postDetails=? and postDate=? ",(new_candidatesTitle,new_language,new_postDetails,new_postDate,candidatesTitle,language,postDetails,postDate))
	conn.commit()
	data = c.fetchall()
	return data




# Track Pages Visited
def create_page_visited_table():
	c.execute('CREATE TABLE IF NOT EXISTS pagetrackTable(pagename TEXT,timeOfvisit TIMESTAMP)')

def add_page_visited_details(pagename,timeOfvisit):
	c.execute('INSERT INTO pagetrackTable(pagename,timeOfvisit) VALUES(?,?)',(pagename,timeOfvisit))
	conn.commit()



# View Details
def view_all_page_visited_details():
	c.execute('SELECT * FROM pagetrackTable')
	data = c.fetchall()
	return data



def loggedin_user_activity():
	c.execute('SELECT * FROM jobPostingTable INNER JOIN userstable ON jobPostingTable.email=userstable.email;')
	data = c.fetchall()
	return data




# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(firstname TEXT,lastname TEXT,email TEXT,password TEXT,school TEXT,year DATE,classlevel TEXT,emphasis TEXT)')


def add_userdata(firstname,lastname,email,password,school,year,classlevel,emphasis):
	c.execute('INSERT INTO userstable(firstname,lastname,email,password,school,year,classlevel,emphasis) VALUES (?,?,?,?,?,?,?,?)',(firstname,lastname,email,password,school,year,classlevel,emphasis))
	conn.commit()

def login_user(email,password):
	c.execute('SELECT * FROM userstable WHERE email =? AND password = ?',(email,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def view_all_user_profiles():
	c.execute('SELECT DISTINCT email FROM userstable')
	data = c.fetchall()
	return data

def get_profile(email):
	c.execute('SELECT * FROM userstable WHERE email="{}"'.format(email))
	data = c.fetchall()
	return data



def login_admin(email,password):
	if (email in ['edgard.almeida@gmail.com','anacristinagazzola@gmail.com','admin@gmail.com']) & (password == "admin101"):
		return True



def edit_user_profile_data(new_firstname,new_lastname,new_email,new_password,new_school,new_year,new_class_level,new_emphasis,firstname,lastname,email,password,school,year,classlevel,emphasis):
	c.execute("UPDATE userstable SET firstname =?,lastname=?, email=?,password=?,school=?,year=?,classlevel=?,emphasis=? WHERE firstname =? and lastname=? and email=? and password=? and school=? and year=? and classlevel=? and emphasis=?",(new_firstname,new_lastname,new_email,new_password,new_school,new_year,new_class_level,new_emphasis,firstname,lastname,email,password,school,year,classlevel,emphasis))
	conn.commit()
	data = c.fetchall()
	return data