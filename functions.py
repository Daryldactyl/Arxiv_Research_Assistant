## General imports
import re
import os
import langchain
from langchain_openai import OpenAI
import streamlit as st

# ## ENVIRONMENTAL VARIABLES
# os.environ['SERPAPI_API_KEY'] = serpapi
# os.environ['OPENAI_API_KEY'] = openai
#
# ## CONNECT THE LLM
# llm = OpenAI(temperature=0.4)

##-------------------------- FUNCTIONS ------------------------------##

# Use LLM to refine User raw Query
from langchain.prompts import PromptTemplate
def create_accurate_query(_query, _llm):
    template = PromptTemplate(
        input_variables=['query'],
        template="""You are a helpful research assistant for machine learning tasks. The user will be finding relevant research papers based on a query of something they want to know more about, are trying to research, or a project they are trying to find help with. The query will be passed along to another llm who will then use this query to find relevant research papers in a research paper database.

        Using this original user query: {query}

        I want you to return a succinct query for the next llm to search research paper archives for a paper that will help the user complete their task. The search should not be task specific but should be specific to the type of network or algorithm the user should use to complete the task. For example a user wanting to create a CNN to classify dog breeds you could consider creating a query for recent CNN algorithms for classification but do not include the specific task of classifying dog breeds. I want you to return ONLY the updated query that you will generate. No other response only the new query. Do not include any quotation marks in your answer
        """
    )

    updated_query = _llm.invoke(template.format(query=_query))
    updated_query = updated_query.content
    updated_query = updated_query.strip('"')
    return updated_query

#EXAMPLE USE CASE
# user_query = "I want to create a model to complete pose estimation for UFC fights"
# updated_query = create_accurate_query(user_query)
# print(updated_query)
####################################################################################################

# Find Arxiv Research papers that best fit user query

from langchain_community.retrievers import ArxivRetriever
def find_arxiv_papers(_query):
    #Paper links for the chain
    arxiv_papers = []
    retriever = ArxivRetriever(load_max_docs=5)
    docs = retriever.invoke(_query)
    num_docs = len(docs)
    for i in range(num_docs):
        meta = docs[i].metadata
        arxiv_papers.append(meta['Entry ID'])

    #URL links for hyperlinking
    updated_urls = []
    for url in arxiv_papers:
        updated_url = re.sub(r'abs', 'pdf', url)
        updated_urls.append(updated_url)
    return arxiv_papers, updated_urls

#EXAMPLE USE CASE
# arxiv_papers, urls = find_arxiv_papers(updated_query)
# print(arxiv_papers)
# print(urls)

####################################################################################################

# Create Folder to save PDF documents in
def create_folder_name(_query, _llm):
    prompt = PromptTemplate(
        input_variables = ['query'],
        template = """I need you to create a simple 1-3 word folder name to save pdf's based on this query: {query}, 
        return only the name of the folder, no further explanation. There should be no quotation marks in the reply"""
    )
    folder_name = _llm.invoke(prompt.format(query=_query))
    folder_name = folder_name.content
    folder_name = folder_name.strip('"')
    return folder_name

#EXAMPLE USE CASE
# folder = create_folder_name(updated_query)
# print(folder)

####################################################################################################

# Download Arxiv papers to folder

import requests
from bs4 import BeautifulSoup
import os
import re

def get_numbers(url):
    pattern = r'/(\d+\.\d+v\d+)$'
    match = re.search(pattern, url)
    if match:
        numbers = match.group(1)
    else:
        numbers = None
    return numbers
def download_pdf_from_arxiv(_url, _download_folder):
    if not os.path.exists(_download_folder):
        os.makedirs(_download_folder)

    number = get_numbers(_url)
    response = requests.get(_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page with status code: {response.status_code}")
        return

    # Check if the content is already a PDF file
    if response.headers['Content-Type'] == 'application/pdf':
        pdf_name = _url.split('/')[-1] + '.pdf'
        pdf_filename = os.path.join(_download_folder, pdf_name)
        with open(pdf_filename, 'wb') as pdf:
            pdf.write(response.content)
        print(f'File downloaded successfully as: {pdf_filename} in {_download_folder} folder')
        return

    # Parse the HTML to find the title
    soup = BeautifulSoup(response.text, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
    else:
        print("No title found.")
        return

    # Clean the title
    pretty_title = re.sub(r'\[[^\]]+\]', '', title).strip()
    title = re.sub(r'[^\w\-_\.]', '', pretty_title)
    title = title.replace(' ', '_')
    print(pretty_title)

    # Find the PDF link
    pdf_link = soup.find('a', class_='mobile-submission-download')
    if pdf_link is None:
        print("No PDF link found.")
        return

    pdf_url = 'https://arxiv.org' + pdf_link.get('href')
    print(f"Downloading PDF from {pdf_url}")

    # Download the PDF file
    pdf_response = requests.get(pdf_url)
    if pdf_response.status_code != 200:
        print(f"Failed to download PDF with status code: {pdf_response.status_code}")
        return

    # Save the PDF file
    pdf_filename = os.path.join(_download_folder, f'{title}.pdf')
    with open(pdf_filename, 'wb') as pdf:
        pdf.write(pdf_response.content)

    print(f'File downloaded successfully as: {pdf_filename} in {_download_folder} folder')
    return number, pretty_title

#EXAMPLE USE CASE
# for paper in arxiv_papers:
#     download_pdf_from_arxiv(paper, folder)

####################################################################################################

#Summarize all PDFs

from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
def summarize_pdf_and_create_db(_folder, _pdf_paths, _llm, _openai_api_key):
    all_pages = []
    summaries = []

    # Load and split documents from each PDF
    for pdf_path in _pdf_paths:
        pdf_path = os.path.join(_folder, pdf_path)
        loader = PyPDFLoader(pdf_path)
        document = loader.load_and_split()
        all_pages.extend(document)

        # Summarize the document
        chain = load_summarize_chain(_llm, chain_type='map_reduce')
        summary = chain.invoke(document)
        summaries.append(summary)

    # Create embeddings for all combined pages
    embeddings = OpenAIEmbeddings(openai_api_key=_openai_api_key)
    db = FAISS.from_documents(all_pages, embeddings)

    return summaries, db

#EXAMPLE USE CASE
# pdfs = os.listdir(folder)
# summaries = []
# dbs = {}
# for pdf in pdfs:
#     pdf_path = os.path.join(folder, pdf)
#     summary, db = summarize_pdf_and_create_db(pdf_path)
#     summaries.append(summary)
#     dbs[pdf] = db
#     print(f"Summary of {pdf}:\n {summary['output_text']}\n")

####################################################################################################

# Make best recommendation based on paper summary
def make_paper_recommendation(_summaries, _query, _llm):
    template = PromptTemplate(
        input_variables=['summaries', 'query'],
        template="""
        Based on these summaries of research papers: {summaries}, I would like for you to recommend
        which paper I should do additional research on in order to complete the task from my query:
        {query}. I would like for you to recommend the number along with the title of the PDF that
        you recommend that would be most useful for the user along with your justification as to why
        this paper would prove the most useful.
        """
    )
    recommendation = _llm.invoke(template.format(summaries=_summaries, query=_query))
    recommendation = recommendation.content
    return recommendation.strip()

def extract_pdf_filename(recommendation):
    # Regular expression pattern to match the filename
    pattern = r'\d{4}\.\d{5}v\d+_[\w\.-]+\.pdf'
    match = re.search(pattern, recommendation)
    if match:
        return match.group(0)
    else:
        return None

#EXAMPLE USE CASE
# cleaned_summaries = [f"{i+1}. {pdf}: {summary['output_text'].strip()}" for i, (summary, pdf) in enumerate(zip(summaries, pdfs))]
# result = '\n'.join(cleaned_summaries)
# recommendation = make_paper_recommendation(result, user_query)
# print(f'Recommendation: {recommendation}')
#
# # Assuming the user selects the recommended paper
# selected_paper = extract_pdf_filename(recommendation)
# print(selected_paper)

####################################################################################################

#EXAMPLE USE CASE
# from langchain.chains.question_answering import load_qa_chain
# selected_db = dbs[selected_paper]
#
# # Example query
# query = "What are the main findings of this paper?"
#
# # Retrieve relevant documents and answer the question
# chain = load_qa_chain(OpenAI(openai_api_key=openai, temperature=0), chain_type="stuff")
# docs = selected_db.similarity_search(query)
# answer = chain.run(input_documents=docs, question=query)
# print(answer)
