# AWS Based Job-Description-and-Resume-Analyzer-with-NLP-and-OpenAI

The application is backed by AWS services.

## Features

### 1. OTP Verification (AWS Lambda)
- Secure access to the application through OTP verification sent to the user's IU email address (`@iu.edu`).
- The OTP functionality is powered by **AWS Lambda**, which handles OTP generation and verification.
- The user must validate their email before proceeding with the analysis.

### 2. Keyword Extraction
- Extracts the most frequent keywords from both the job description and the uploaded resume.
- Displays matching and missing keywords, highlighting areas where the resume aligns with or needs improvement based on the job description.

### 3. Similarity Comparison
- Compares the job description and the resume using **SentenceTransformers**, a machine learning model for natural language processing.
- Calculates a similarity score between the two texts to indicate how closely the resume matches the job description.

### 4. Resume Feedback
- Provides personalized feedback to improve the resume using **OpenAI's GPT-3.5**.
- Focuses on missing keywords, formatting, and content suggestions to tailor the resume for the job.

### 5. Word Cloud Visualization
- Generates word clouds for both the job description and the resume to visualize the most frequent words.
- Helps identify important terms and ensure alignment between the two documents.

## How to Use

1. **Set Up OTP Verification**:
   - Upon visiting the app, the user is prompted to enter their IU email.
   - An OTP is sent to the provided email address for verification.
   
2. **Enter Job Description**:
   - Paste the job description into the text box provided in the app.

3. **Upload Resume**:
   - Upload your resume in **PDF** format for analysis.

4. **Analyze**:
   - Click the **Analyze** button to start the analysis.
   - The app will extract keywords, compare texts, calculate similarity, and generate feedback.

5. **View Results**:
   - The app displays a similarity score, matching and missing keywords, and personalized resume feedback.
   - Word clouds are generated for both the job description and the resume to help visualize key terms.

## Technologies Used

- **spaCy**: NLP library for text processing.
- **Sentence-Transformers**: Used for generating sentence embeddings and comparing text similarity.
- **OpenAI GPT-3.5**: Provides personalized feedback for resume improvement.
- **AWS Lambda**: Handles OTP generation and verification, ensuring secure access to the application.
- **pdfminer**: Library to extract text from PDF resumes.
- **WordCloud**: Generates word cloud visualizations.
- **Matplotlib**: Used to display word clouds.

## Installation

To run the project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/SaiDhanushKolla777/Job-Description-and-Resume-Analyzer-with-NLP-and-OpenAI.git
cd Job-Description-and-Resume-Analyzer-with-NLP-and-OpenAI
```

### 2. Install Dependencies

Create a virtual environment and install the required libraries:

```bash
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

### 3. Set Up OpenAI API Key

To use OpenAI's GPT-3.5 for resume feedback, you need to set your OpenAI API key:

```python
openai.api_key = 'your-openai-api-key'
```

### 4. Set Up AWS Lambda

To enable OTP verification, you'll need to configure AWS Lambda and API Gateway for handling OTP generation and verification.

1. **Create an AWS Lambda function** that generates and verifies OTPs.
2. **Set up an API Gateway** to expose the Lambda function as an endpoint for OTP generation and verification.
3. Update the **`verify_otp_url`** and **`invoke_url`** in your code with the API Gateway endpoint URLs.



## Contributing

Feel free to fork the repository and submit pull requests if you have improvements or new features to suggest. Please make sure to update the documentation and include tests for any new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
