from flask import Flask, render_template, request
import pandas as pd
import os
import google.generativeai as genai

# Setting Google API key for the generative model
os.environ['GOOGLE_API_KEY'] = 'YOUR_API_KEY'  

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# Load the CSV data into memory
CSV_FILE_PATH = 'final.csv' 
data = pd.read_csv(CSV_FILE_PATH)

def main_summarize(text):
    response = model.generate_content(f"Summarize the following content: {text}")
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    index = request.form.get('index', '').strip()
    
    if not index.isdigit():
        return "Error: Invalid index. Please enter a numeric value."

    index = int(index)

    # Check if the index is within the valid range
    if index < 0 or index >= len(data):
        return "Error: Index out of range. Please enter a valid index number."

    # Fetch the text from the specified index in the CSV file
    article_text = data.iloc[index]['article']  # Assuming 'article' is the column name containing the text

    if not article_text:
        return "Error: No text found at the specified index."

    # Perform summarization 
    summarized_text = main_summarize(article_text)

    # Render the result template with the original and summarized text
    return render_template('result.html', original_text=article_text, summarized_text=summarized_text)

if __name__ == '__main__':
    app.run(debug=True)
