# Arxiv_Research_Assistant

## **Introduction**

The Arxiv Research Assistant is a sophisticated tool tailored to support machine learning researchers in their exploration of academic literature. This README serves as a comprehensive guide to help users set up the environment, install dependencies, and seamlessly navigate through the program's functionalities.

## **Functionality Overview**

The Arxiv Research Assistant streamlines the research process by transforming raw user queries into refined search parameters. Utilizing advanced language models (LLMs), the assistant crafts precise queries to scour arXiv.org for the most pertinent research papers. Once identified, the assistant automatically downloads the PDFs into a local repository.

Each PDF is meticulously summarized, providing users with succinct insights into the paper's content. Hyperlinks are generated for easy access to the full papers, allowing users to efficiently navigate through the research landscape. Additionally, the assistant leverages its analytical capabilities to recommend the most relevant paper based on the user's original query.

For further engagement with the papers, the assistant offers a "Chat with Paper" feature. This functionality enables users to interact directly with the saved PDFs stored in a database. Users can seek clarification, pose inquiries, or extract specific information from the papers, enhancing their understanding and research capabilities.

## **Web App, Docker Container, or Build Local without Container**

To just get started using the assistant you can open the [streamlit webapp](https://arxivresearchassistant.streamlit.app/).
- **Note:** Running the research request in the web app takes about 3-5 minutes but once the research is complete you can speak to the assistant and receive a response within a second.

If you would rather run the assistant locally please follow the setup instructions!

## **Docker Container**

To spin up the research assistant in a docker container follow these steps:
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

### *3. Build the Container*
Navigate to the project directory and build the container.

```bash
cd Arxiv_Research_Assistant
```
```bash
docker build -t arxiv-research-assistant .
```

### *4. Run the Container and get to Researching!*
Run the container on your desired port then navigate to the local host instance.

```bash
docker run -d -p 8501:8501 arxiv-research-assistant
```
In your chosen internet browser navigate to:
http://localhost:8501/

HAVE FUN! Navigate to the Usage Section for help

## **Build Local without Container**
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

**Note: To make another research request just type in your new reqest in the Launch Research form. Session states will be cleared and generate papers based on the new request**

## Usage
To maximize the effectiveness of the Arxiv Research Assistant, users are encouraged to follow the instructions provided in this README. By adhering to the setup guidelines and installing the necessary dependencies, users can seamlessly harness the power of the assistant to streamline their research endeavors.

- ### Using the Streamlit Web App
  For users who prefer to use the web app rather than running locally, there is an additional parameter before getting access to the assistant. You must first enter your Open AI API key. For safety, I recommend revoking the key after using the assistant. Please note the research request takes between 3-5 minutes to run initially on the web app but once research is complete the assistant can return answers to any questions within a second.
  ![Screenshot 1](/app_screenshots/api_key_input.png)

- ###  **Making a Request**
  To initiate a request, simply input the topic of your current project or the subject you're actively researching, then click "Launch Request". This action triggers the Arxiv Research Assistant to begin its search process.
  ![Screenshot 2](/app_screenshots/research_task.png)

- ### **Explore Relevant Papers**
  Once the Assistant completes downloading relevant papers, building the reference database, and generating summaries, three tabs are generated. The first tab, "Explore Relevant Papers", provides hyperlinks to each paper. Clicking on a hyperlink redirects the user to the corresponding PDF for thorough review. Additionally, each paper is accompanied by a summary expander for quick insights.
  ![Screenshot 3](/app_screenshots/found_papers.png)

- ### **Assistant's Recommendation**
  After scanning all documents, the AI Research Assistant formulates a recommendation based on the user's request and the paper contents. This recommendation suggests the paper best suited to address the user's specific use case, facilitating further research efforts.
  ![Screenshot 4](/app_screenshots/assistant_recommendation.png)

- ### **Chatting with Research Paper**
  In the "Chatting with Research Paper" tab, users select the relevant paper from the dropdown menu. They can then pose questions in the text box. Upon clicking "Request", the research assistant employs advanced RAG techniques to provide the best possible answers. Users can continue asking questions or switch to another paper using the dropdown menu.
  ![Screenshot 5](/app_screenshots/assistant_chat.png)
  
