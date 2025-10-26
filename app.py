import streamlit as st
import spacy
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from collections import Counter
import openai
from sentence_transformers import SentenceTransformer, util
import io
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import json

# Disable PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load NLP models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set OpenAI API key
# Enter your OpenAI API Key
openai.api_key = ''


# OTP verification logic

def otp_verification():
    st.subheader("OTP Verification")
    user_email = st.text_input("Enter your IU email address:")
    if user_email:
        send_button = st.button('Send OTP')
        if send_button:
            if user_email.endswith('@iu.edu'):  # Validate IU email address
                otp_response = send_otp_request(user_email)
                if otp_response.status_code == 200:
                    st.success('OTP has been sent to your email address.')
                    st.session_state['otp_sent'] = True
                else:
                    st.error('Something went wrong while sending OTP.')
            else:
                st.error('Please enter a valid IU email address.')

    if st.session_state.get('otp_sent', False):
        user_otp = st.text_input("Enter the OTP:")
        verify_button = st.button('Verify OTP')
        if verify_button:
            if verify_otp(user_email, user_otp):
                st.success('OTP verified successfully!')
                st.session_state['otp_verified'] = True
            else:
                st.error('Incorrect OTP. Please try again.')


def verify_otp(email, otp):
    verify_otp_url = ''
    data = {'email': email, 'otp': otp}
    
    # Make the POST request to the API endpoint
    response = requests.post(verify_otp_url, json=data)
    
    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Directly work with the response body as a string
        # Assuming your Lambda function returns a simple string within the body
        response_body = response.text  # Use .text to get the raw string response
        
        # Assuming the successful response body text includes "OTP verification successful."
        if "OTP verification successful." in response_body:
            return True
        else:
            return False
    else:
        # Log the error or inform the user
        print(f"Failed to verify OTP. Status code: {response.status_code}, Response: {response.text}")
        return False

# Function to send OTP request to your AWS Lambda function
def send_otp_request(email):
    # Replace with the invoke URL you received from API Gateway
    invoke_url = ''
    response = requests.post(invoke_url, json={'email': email})
    return response


def main_app():
    st.title("Job Description and Resume Analyzer")

    # Main layout adjustment for input, analysis, and word clouds
    col_main, col_word_cloud = st.columns([2, 1])




    with col_main:
        col_input, col_analysis = st.columns([1, 1])
        with col_input:
            job_description = st.text_area("Job Description", "Paste the job description here.")
            resume_file = st.file_uploader("Upload Resume", type=['pdf'])
            num_keywords_to_display = st.slider("Number of Keywords to Display", min_value=5, max_value=30, value=20)

        with col_analysis:
            if st.button("Analyze"):
                if job_description and resume_file:
                    with st.spinner("Analyzing..."):
                        time.sleep(3)  # Simulating processing time

                        # Extract text from uploaded resume
                        resume_text = extract_text(io.BytesIO(resume_file.getvalue()))

                        # Extract keywords
                        job_desc_keywords = extract_keywords(job_description, num_keywords_to_display)
                        resume_keywords = extract_keywords(resume_text, num_keywords_to_display)

                        # Compare for similarity
                        similarity_score = compare_texts_deep(job_description, resume_text)

                        # Matching keywords
                        matching_keywords = set(resume_keywords) & set(job_desc_keywords)
                        missing_keywords = set(job_desc_keywords) - set(resume_keywords)

                        # Display Keywords Analysis and Resume Feedback
                        st.subheader("Keywords Analysis")
                        st.write(f"**Similarity Score:** {similarity_score:.2f}")
                        st.write("**Matching Keywords:**", ', '.join(matching_keywords))
                        st.write("**Missing Keywords:**", ', '.join(missing_keywords))

                        feedback = generate_resume_feedback(job_description, resume_text, list(missing_keywords))
                        st.subheader("Resume Feedback")
                        st.markdown(feedback)

                else:
                    st.error("Please upload a resume and paste a job description.")

    with col_word_cloud:
        st.subheader("Word Clouds")
        if 'job_description' in locals() and job_description:
            fig, ax = plt.subplots(figsize=(5, 5))
            job_desc_wordcloud = WordCloud(width=400, height=400, background_color='white').generate(job_description)
            ax.imshow(job_desc_wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            st.caption("Job Description Word Cloud")

        if 'resume_text' in locals() and resume_file:
            fig, ax = plt.subplots(figsize=(5, 5))
            resume_wordcloud = WordCloud(width=400, height=400, background_color='white').generate(resume_text)
            ax.imshow(resume_wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
            st.caption("Resume Word Cloud")




def extract_keywords(text, num_keywords=20):
    text = re.sub(r'[^\w\s]', '', text.lower())
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    counted_words = Counter(filtered_words)
    keywords = counted_words.most_common(num_keywords)
    return [kw for kw, _ in keywords]

def compare_texts_deep(text1, text2):
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
    return cosine_scores.item()

def generate_resume_feedback(job_description, resume_text, missing_keywords):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Given a job description: '{job_description}' and a resume text: '{resume_text}', with missing keywords: {', '.join(missing_keywords)}, provide detailed feedback on how the resume can be improved to match the job description better."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or the latest suitable chat model
        messages=conversation,
        temperature=0.5,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    if response.choices:
        assistant_reply = response.choices[0].message['content']
    else:
        assistant_reply = "Sorry, I couldn't generate feedback at this time."

    return assistant_reply.strip()

def setup_ui():
    # Initialize session states if not present
    st.session_state.setdefault('otp_sent', False)
    st.session_state.setdefault('otp_verified', False)

    if st.session_state['otp_verified']:
        main_app()
    else:
        otp_verification()


setup_ui()
