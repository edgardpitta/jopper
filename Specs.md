### Job/Candidate Analyzer App
Create a website to use NLP to analyze a job posting, compare it to the candidate’s career materials (presentation pitch, CV, letter of interest, etc.) and provide a matching analysis and similarity score between them. 

Each of the following items should be in a different page.

#### 1. Authentication
User input fields
        a. Name - text
        b. Surname - text
        c. Email - email
        d. Campus/School  - dropdown
        e. Year – date MM-YYYY
        f. Class – dropdown 
        g. Emphasis - dropdown

When the user log in, they can visualize, delete or change all analysis they did (CRUD).
Types of accounts: user or admin

#### 2. Job Posting
Users upload pdf or txt files with job postings. 

Fields:
    • Job_Title – text
    • Determine Language – en, fr, pt
    • File upload


NLP:
    • Text cleaning (remove stopwords, numbers, punctuations, special chars) and tokenization
    • TF-IDF analysis
    • Create db job_posting with token counting
    • Plot Wordcloud with most common TF-IDF tokens
    • Show a list of most common words

* List of stopwords should be updated by us

#### 3. Candidate Material
User upload a pdf file OR use a field to paste, write and edit his career material.

NLP:
    • Convert the pdf file to txt and show it, if it is the case; otherwise use the text provided in the text field
    • Validate if the candidate material is in the same language of the job posting provided. If not, show an error message.
    • Text cleaning (remove stopwords, numbers, punctuations, special chars) and tokenization
    • Create Wordcloud with most common tokens
    • Create db user_info with token counting
    • Show table with 20 most common tokens
    • Show table with the ten most common competencies (match with a list we will create and update)
    • Show chart with Parts of Speech – PoS tags
    • Sentiment analysis (polarity and subjectivity)

    4. Candidate/Job Posting Match
    • User select the job posting he wants to compare with 
    • Show the Job Title the user provided
    • Show wordclouds (job posting and candidate material) side by side
    • Show a table with the most common tokens in job posting and user info, indexed by job_posting (we want to see if the most common tokens in the job posting appear in the candidate material)
    • Calculate a similarity score of the candidate material compared with the job posting (initial score). Calculate a new score(s) after student changes its career materials (improved score) Salve both the initial and all the improved scores.
    • Other analysis you may find valid.

    5. Admin Reports (Only admin users can see these reports)
Create reports aggregated by the fields (alone or combined):
        a. Campus/School  - dropdown
        b. Year – date MM-YYYY
        c. Class – dropdown 
        d. Specialization
        e. Job title
#### Reports:
    • Show a table/wordcloud with the most common tokens of a certain group of users  according to the parameters above (for instance: all students of the same class, or the same year, or a combination of both)
    • Plot a graph with the combined sentiment analysis of a certain group of users
    • Plot a graph with the combined subjectivity analysis of a certain group of users 
    • Show a table with the matching score of all users of a certain group of users