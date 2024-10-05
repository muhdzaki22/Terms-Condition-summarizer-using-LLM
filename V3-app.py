from flask import Flask, render_template, request
from pdfminer.high_level import extract_text
import cohere
import os

# Initialize Flask app
app = Flask(__name__)

# Set your Cohere API key
cohere_api_key = 'MXZsoQ7cjPVTwu2l9thRoiNNkpmxHWbpbXPGx87G'  # Replace with your actual Cohere API key
co = cohere.Client(cohere_api_key)

# Extract text from a PDF using pdfminer
def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

# Summarize text using Cohere API
def summarize_text(text):
    response = co.summarize(
        text=text,
        length="medium",  # Can also try "long" or "short"
        format="bullets",  # Experiment with "paragraph" for a different structure
        temperature=0.5,  # Adjust temperature for creativity (higher) or determinism (lower)
        extractiveness="low"  # Try "high" for more extracted content or "low" for more abstraction
    )
    
    # Split the summary by line and join with <br> tags for HTML rendering
    bullet_points = response.summary.split("\n")  # Assuming bullets are separated by new lines
    formatted_summary = "<br><br>".join(bullet_points)  # Join with <br> tags

    return formatted_summary

# Flask route to handle the uploaded text or PDF
@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            file_path = "temp_pdf.pdf"
            uploaded_file.save(file_path)
            content = extract_text_from_pdf(file_path)
            summary = summarize_text(content)  # Use Cohere to summarize the content

    return render_template('V3-index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
