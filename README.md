# Arxiv_Research_Assistant

## **Introduction**

The Arxiv Research Assistant is a sophisticated tool tailored to support machine learning researchers in their exploration of academic literature. This README serves as a comprehensive guide to help users set up the environment, install dependencies, and seamlessly navigate through the program's functionalities.

## **Functionality Overview**

The Arxiv Research Assistant streamlines the research process by transforming raw user queries into refined search parameters. Utilizing advanced language models (LLMs), the assistant crafts precise queries to scour arXiv.org for the most pertinent research papers. Once identified, the assistant automatically downloads the PDFs into a local repository.

Each PDF is meticulously summarized, providing users with succinct insights into the paper's content. Hyperlinks are generated for easy access to the full papers, allowing users to efficiently navigate through the research landscape. Additionally, the assistant leverages its analytical capabilities to recommend the most relevant paper based on the user's original query.

For further engagement with the papers, the assistant offers a "Chat with Paper" feature. This functionality enables users to interact directly with the saved PDFs stored in a database. Users can seek clarification, pose inquiries, or extract specific information from the papers, enhancing their understanding and research capabilities.

## **Setup**
### *1. Create a Virtual Environment (Optional but Recommended)*
It's a good practice to work within a virtual environment to manage project dependencies.

```bash
# Create a virtual environment
python3 -m venv env
```
```bash
# Activate the virtual environment
source env/bin/activate
```

### *2. Clone the Repository*
Clone the Arxiv Research Assistant repository to your local machine.

```bash
git clone https://github.com/Daryldactyl/Arxiv_Research_Assistant.git
```

### *3. Install Dependencies*
Navigate to the project directory and install the required dependencies from the requirements.txt file.

```bash
cd Arxiv_Research_Assistant
pip install -r requirements.txt
```

### *4. Insert OpenAI API Key*
You will need to open the python file in your chosen IDE and insert this line in app.py:
```python
openai = 'your_api_key'
```
above this line:
```python
os.environ['OPENAI_API_KEY'] = openai
```
and comment out the import:
```python
from secret_keys import openai
```

###  *5. Run The App* 
While in the project directory launch the streamlit app by running:
```bash
streamlit run app.py
```

**Note: To make another research request you will need to close the app with ^C then run the streamlit app again as request speed is optimized by saving the session state**

## Usage
To maximize the effectiveness of the Arxiv Research Assistant, users are encouraged to follow the instructions provided in this README. By adhering to the setup guidelines and installing the necessary dependencies, users can seamlessly harness the power of the assistant to streamline their research endeavors.

- ###  **Making a Request**
  To initiate a request, simply input the topic of your current project or the subject you're actively researching, then click "Launch Request". This action triggers the Arxiv Research Assistant to begin its search process.
  ![Screenshot 1](/app_screenshots/make_request.png)

- ### **Explore Relevant Papers**
  Once the Assistant completes downloading relevant papers, building the reference database, and generating summaries, three tabs are generated. The first tab, "Explore Relevant Papers", provides hyperlinks to each paper. Clicking on a hyperlink redirects the user to the corresponding PDF for thorough review. Additionally, each paper is accompanied by a summary expander for quick insights.
  ![Screenshot 2](/app_screenshots/relevant_papers.png)

- ### **Assistant's Recommendation**
  After scanning all documents, the AI Research Assistant formulates a recommendation based on the user's request and the paper contents. This recommendation suggests the paper best suited to address the user's specific use case, facilitating further research efforts.
  ![Screenshot 3](/app_screenshots/recommendation.png)

- ### **Chatting with Research Paper**
  In the "Chatting with Research Paper" tab, users select the relevant paper from the dropdown menu. They can then pose questions in the text box. Upon clicking "Request", the research assistant employs advanced RAG techniques to provide the best possible answers. Users can continue asking questions or switch to another paper using the dropdown menu.
  ![Screenshot 4](/app_screenshots/chat_with_paper.png)
  
