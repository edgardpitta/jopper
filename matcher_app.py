  # 4. Candidate/Job Posting Match
  #   • User select the job posting he wants to compare with 
  #   • Show the Job Title the user provided
  #   • Show wordclouds (job posting and candidate material) side by side
  #   • Show a table with the most common tokens in job posting and user info, indexed by job_posting (we want to see if the most common tokens in the job posting appear in the candidate material)
  #   • Calculate a similarity score of the candidate material compared with the job posting (initial score). Calculate a new score(s) after student changes its career materials (improved score) Salve both the initial and all the improved scores.
  #   • Other analysis you may find valid.

# core pkgs
import streamlit as st 


from app_utils import (view_all_jobposting_details_data,view_all_candidates_details_data,get_candidate_by_jobtitle,get_post_by_jobtitle,view_all_jobtitles_for_jobposting,view_all_jobtitles_for_candidates,get_candidate_by_jobtitle)
from app_utils import (view_all_jobtitles_for_candidates_for_loggedin_user,view_all_jobtitles_for_jobposting_for_loggedin_user)
from func_utils import (get_most_common_tokens_as_df,plot_wordcloud,preprocess_text,__get_wordcloud,__get_most_common_tokens,cosine_sim,analyze_sentiment,analyze_sentiment_to_df,plot_comparisons)

# Data Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib 
matplotlib.use('Agg')
from matplotlib_venn import venn2
import altair as alt
import time 
timestr = time.strftime("%Y%m%d-%H%M%S")


def compare_tokens(tokensA,tokensB):
  setA = set(tokensA)
  setB = set(tokensB)
  disimilar_tokens = [x for x in setA if x not in setB]
  # similar_tokens = list(setA.intersection(setB))
  similar_tokens = [x for x in setA if x in setB ]
  results = {'similar_tokens':similar_tokens,'disimilar_tokens':disimilar_tokens}
  return results

def venn_diagram(a, b, labels=['A', 'B',]):
    a = set(a)
    b = set(b)
  
    only_a = len(a - b)
    only_b = len(b - a)

    only_a_b = len(a & b)
    a_b = len(a & b )

    vfig = plt.figure()
    venn2(subsets=(only_a, only_b, only_a_b, a_b), set_labels=labels)
    st.pyplot(vfig)




def MatcherPage():
  st.subheader("Match Candidate and Job Posting")

  # jobpost_list = ["Dev1","Dev2","Datascience"]
  jobpost_list = [i[0] for i in view_all_jobtitles_for_jobposting()]
  jobtitle_choice = st.selectbox("Job Titles",jobpost_list)


  candidates_list = [i[0] for i in view_all_jobtitles_for_candidates()]
  candidates_choice = st.selectbox("Candidate Profiles",candidates_list)

  # Layout for comparison
  col_job,col_candidate = st.columns(2)


  with col_job:
    st.success("Job Posting")
    job_data = get_post_by_jobtitle(jobtitle_choice)
    st.write(job_data)
    job_raw_text = job_data[0][3]
    processed_text1 = preprocess_text(str(job_raw_text).lower())
    df_job = get_most_common_tokens_as_df(processed_text1)
    st.dataframe(df_job)


  with col_candidate:
    st.info("Candidate Material")
    candidates_data = get_candidate_by_jobtitle(candidates_choice)
    st.write(candidates_data)
    candidates_raw_text = candidates_data[0][3]
    processed_text2 = preprocess_text(str(candidates_raw_text).lower())
    df_candidates = get_most_common_tokens_as_df(processed_text2)
    st.dataframe(df_candidates)



  with st.expander("Similarity Score"):
    sim_score = cosine_sim(processed_text1,processed_text2)
    st.write("Jobs vs Candidate:{}".format(sim_score))


  with st.expander("Compare Tokens"):
    st.info("Comparison")
    # df_diff = df_job.compare(df_candidates)
    # st.dataframe(df_diff)
    tokens_Jobs = df_job['tokens'].tolist()
    tokens_candidates = df_candidates['tokens'].tolist()
    results = compare_tokens(tokens_Jobs,tokens_candidates)
    st.write(results)

    # Wordcloud for Disimilar
    st.info("Wordcloud:Disimilar Tokens")
    disimilar_tokens_for_comparison = ' '.join(results['disimilar_tokens'])
    plot_wordcloud(disimilar_tokens_for_comparison)

    # Wordcloud for Similar
    st.info("Wordcloud:Similar Tokens")
    if len(results['similar_tokens']) >=1:
      similar_tokens_for_comparison = ' '.join(results['similar_tokens'])
      plot_wordcloud(similar_tokens_for_comparison)
    else:
      st.warning("No Similar Tokens")


  with st.expander("Compare Wordcloud"):

    token_num = 6
    figsize=(20,10)
    xt, yt = __get_most_common_tokens(processed_text1, num=token_num)
    xs, ys = __get_most_common_tokens(processed_text2, num=token_num)
    jobs_wordcloud = __get_wordcloud(processed_text1)
    candidate_wordcloud = __get_wordcloud(processed_text2)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Subplots[Vertical]")
    ax1.bar(xt, yt)
    ax1.set_title("Tokens Frequency[Jobs]")
    ax1.tick_params(labelrotation=45)
    ax2.bar(xs, ys,color="orange")
    ax2.set_title("Tokens Frequency[Candidate]")
    ax2.tick_params(labelrotation=45)
    ax3.imshow(jobs_wordcloud, interpolation="bilinear")
    ax3.set_title("Wordcloud[Jobs]")
    ax4.imshow(candidate_wordcloud, interpolation="bilinear")
    ax4.set_title("Wordcloud[Candidate]")
    st.pyplot(fig)
    st.info("Saved Plot")
    filename_to_save_as = 'comparison_plot_{}.pdf'.format(timestr)
    plot_comparisons(processed_text1,processed_text2,filename=filename_to_save_as)


  with st.expander("Sentiment Analysis"):
    results_for_sentiment = analyze_sentiment_to_df(candidates_raw_text)
    st.write(results_for_sentiment)

    c = alt.Chart(results_for_sentiment).mark_bar().encode(
    x='polarity',
    y='subjectivity')
    st.altair_chart(c,use_container_width=True)
   


def MatcherPage_For_LoggedIn_Email(email):
  st.subheader("Match Candidate and Job Posting")

  # jobpost_list = ["Dev1","Dev2","Datascience"]
  jobpost_list = [i[0] for i in view_all_jobtitles_for_jobposting_for_loggedin_user(email)]
  jobtitle_choice = st.selectbox("Job Titles",jobpost_list)


  candidates_list = [i[0] for i in view_all_jobtitles_for_candidates_for_loggedin_user(email)]
  candidates_choice = st.selectbox("Candidate Profiles",candidates_list)

  # Layout for comparison
  col_job,col_candidate = st.columns(2)


  with col_job:
    st.success("Job Posting")
    job_data = get_post_by_jobtitle(jobtitle_choice)
    st.write(job_data)
    job_raw_text = job_data[0][3]
    processed_text1 = preprocess_text(str(job_raw_text).lower())
    df_job = get_most_common_tokens_as_df(processed_text1)
    st.dataframe(df_job)


  with col_candidate:
    st.info("Candidate Material")
    candidates_data = get_candidate_by_jobtitle(candidates_choice)
    st.write(candidates_data)
    candidates_raw_text = candidates_data[0][3]
    processed_text2 = preprocess_text(str(candidates_raw_text).lower())
    df_candidates = get_most_common_tokens_as_df(processed_text2)
    st.dataframe(df_candidates)



  with st.expander("Similarity Score"):
    sim_score = cosine_sim(processed_text1,processed_text2)
    st.write("Jobs vs Candidate:{}".format(sim_score))


  with st.expander("Compare Tokens"):
    st.info("Comparison")
    # df_diff = df_job.compare(df_candidates)
    # st.dataframe(df_diff)
    tokens_Jobs = df_job['tokens'].tolist()
    tokens_candidates = df_candidates['tokens'].tolist()
    results = compare_tokens(tokens_Jobs,tokens_candidates)
    st.write(results)

    # Wordcloud for Disimilar
    st.info("Wordcloud:Disimilar Tokens")
    disimilar_tokens_for_comparison = ' '.join(results['disimilar_tokens'])
    plot_wordcloud(disimilar_tokens_for_comparison)

    # Wordcloud for Similar
    st.info("Wordcloud:Similar Tokens")
    if len(results['similar_tokens']) >=1:
      similar_tokens_for_comparison = ' '.join(results['similar_tokens'])
      plot_wordcloud(similar_tokens_for_comparison)
    else:
      st.warning("No Similar Tokens")


  with st.expander("Compare Wordcloud"):

    token_num = 6
    figsize=(20,10)
    xt, yt = __get_most_common_tokens(processed_text1, num=token_num)
    xs, ys = __get_most_common_tokens(processed_text2, num=token_num)
    jobs_wordcloud = __get_wordcloud(processed_text1)
    candidate_wordcloud = __get_wordcloud(processed_text2)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle("Subplots[Vertical]")
    ax1.bar(xt, yt)
    ax1.set_title("Tokens Frequency[Jobs]")
    ax1.tick_params(labelrotation=45)
    ax2.bar(xs, ys,color="orange")
    ax2.set_title("Tokens Frequency[Candidate]")
    ax2.tick_params(labelrotation=45)
    ax3.imshow(jobs_wordcloud, interpolation="bilinear")
    ax3.set_title("Wordcloud[Jobs]")
    ax4.imshow(candidate_wordcloud, interpolation="bilinear")
    ax4.set_title("Wordcloud[Candidate]")
    st.pyplot(fig)
    st.info("Saved Plot")
    filename_to_save_as = 'comparison_plot_{}.pdf'.format(timestr)
    plot_comparisons(processed_text1,processed_text2,filename=filename_to_save_as)


  with st.expander("Sentiment Analysis"):
    results_for_sentiment = analyze_sentiment_to_df(candidates_raw_text)
    st.write(results_for_sentiment)

    c = alt.Chart(results_for_sentiment).mark_bar().encode(
    x='polarity',
    y='subjectivity')
    st.altair_chart(c,use_container_width=True)


















    