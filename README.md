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
You will need to open the python file in your chosen IDE and change this line in app.py:
```python
os.environ['OPENAI_API_KEY'] = openai
```
to this:
```python
openai = 'your_api_key'
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

## Usage
To maximize the effectiveness of the Arxiv Research Assistant, users are encouraged to follow the instructions provided in this README. By adhering to the setup guidelines and installing the necessary dependencies, users can seamlessly harness the power of the assistant to streamline their research endeavors.

### **Making a Request**
