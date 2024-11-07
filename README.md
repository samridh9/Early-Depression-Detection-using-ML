<h1>Early Depression Detection using ML</h1>

<p>This project aims to detect early signs of depression through machine learning models, leveraging natural language processing (NLP) techniques to analyze text data. The tool is designed to help identify depression indicators by processing keywords and patterns within written content.</p>

<h2>Features</h2>
<ul>
  <li><strong>NLP-based Text Analysis</strong>: Identifies concerning words and phrases linked to depressive symptoms.</li>
  <li><strong>Predictive Models</strong>: Utilizes Logistic Regression and XGBoost classifiers trained to detect signs of depression.</li>
  <li><strong>Streamlit Interface</strong>: An easy-to-use web interface for testing and demonstrating model predictions.</li>
</ul>

<h2>Files Overview</h2>
<ul>
  <li><code>app.py</code>: Main application file for the Streamlit interface.</li>
  <li><code>prediction.py</code>: Core logic for processing and predicting based on input text.</li>
  <li><code>danger_words.py</code>: Contains keywords associated with depressive language.</li>
  <li>Pre-trained models (<code>logistic_model.sav</code>, <code>xgb_model.sav</code>): Used for predictions.</li>
</ul>
