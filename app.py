import streamlit as st
from secret_keys import openai
import re
import os
import langchain
from langchain.chat_models import ChatOpenAI
from functions import (create_accurate_query, find_arxiv_papers,
                       create_folder_name, download_pdf_from_arxiv, summarize_pdf_and_create_db,
                       make_paper_recommendation)

# Set environmental variables
os.environ['OPENAI_API_KEY'] = openai

# Connect the LLM
llm = ChatOpenAI(temperature=0.4)

# ------------------------ VERIFY CONNECTION -----------------------------------
# # Function to verify connection
# def verify_connection():
#     response = llm.invoke('How are you today?')
#     content = response.content
#     st.write(content)

# verify_connection()

# -----------------------------------------------------------------------------
def download_pdfs(_arxiv_papers, _folder):
    numbers = []
    for paper_url in _arxiv_papers:
        print(f"Downloading PDF from: {paper_url}")
        number = download_pdf_from_arxiv(paper_url, _folder)
        numbers.append(number)
    downloaded_pdfs = os.listdir(_folder)
    print(f"Downloaded PDFs: {downloaded_pdfs}")
    return downloaded_pdfs, numbers

def clear_states():
    states = ['arxiv_papers', 'urls', 'folder', 'pdfs', 'numbers', 'summaries', 'db', 'recommendation']
    for state in states:
        del st.session_state[state]

if __name__ == '__main__':
    # Streamlit app
    st.markdown('# 📚 Arxiv Research Assistant 🤖')

    # Research Form
    with st.form('Research Task'):
        user_query = st.text_area('What task are you working on or would like to research further?',
                                    height=200,
                                    placeholder="ex. I'm trying to build a CNN classifier that can differentiate between cats and dogs.")

        research_button = st.form_submit_button(label='Launch Research')

    if research_button and user_query:
        clear_states()
        # Refine user Query
        updated_query = create_accurate_query(user_query, llm)

        # Find arxiv papers
        arxiv_papers, urls = find_arxiv_papers(updated_query)

        # Create a Folder to save papers to
        folder = create_folder_name(updated_query, llm)

        # Download Arxiv PDFs
        pdfs, numbers = download_pdfs(arxiv_papers, folder)

        #Save session state
        st.session_state['arxiv_papers'] = arxiv_papers
        st.session_state['urls'] = urls
        st.session_state['folder'] = folder
        st.session_state['pdfs'] = pdfs
        st.session_state['numbers'] = numbers

    if 'arxiv_papers' in st.session_state:
        arxiv_papers = st.session_state['arxiv_papers']
        urls = st.session_state['urls']
        folder = st.session_state['folder']
        pdfs = st.session_state['pdfs']
        numbers = st.session_state['numbers']

        # Create summaries and save to databases

        tab1, tab2, tab3 = st.tabs(['Relevant Papers', 'Assistant Recommendation', 'Chat with Paper'])

        with tab1:
            if 'summaries' not in st.session_state:
                summaries, db = summarize_pdf_and_create_db(folder, pdfs, llm, openai)
                st.session_state['summaries'] = summaries
                st.session_state['db'] = db
            summaries = st.session_state['summaries']
            db = st.session_state['db']

            for number, summary, pdf in zip(numbers,summaries,pdfs):
                hyperlink = f"http://arxiv.org/pdf/{number}"
                st.markdown(f'#### [{pdf}]({hyperlink})')
                with st.expander(f'Summary of Paper'):
                    st.markdown(f'*{summary["output_text"]}*')

        with tab2:
            if 'recommendation' not in st.session_state:
                cleaned_summaries = [f"{i+1}. {pdf}: {summary['output_text'].strip()}" for i, (summary, pdf) in enumerate(zip(summaries, pdfs))]
                result = '\n'.join(cleaned_summaries)
                recommendation = make_paper_recommendation(result, user_query, llm)
                st.session_state['recommendation'] = recommendation
            recommendation = st.session_state['recommendation']
            st.markdown(f'**{recommendation}**')

        with tab3:
            from langchain.chains.question_answering import load_qa_chain

            selected_paper = st.selectbox('Which paper are you referencing?', options=pdfs, index=0)

            with st.form('Chat with paper'):

                query = st.text_area(f'What questions do you have about {selected_paper}?',
                                     height=100,
                                     placeholder='ex. What are the findings in this paper?')
                question = f'In reference to {selected_paper}: {query}'
                question_button = st.form_submit_button(label='Request')

                # Retrieve relevant documents and answer the question
                if question_button:
                    chain = load_qa_chain(llm, chain_type="stuff")
                    docs = db.similarity_search(question)
                    answer = chain.run(input_documents=docs, question=question)
                    st.write(answer)


