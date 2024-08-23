import os
import requests
import streamlit as st
from dotenv import load_dotenv
import jsonlines

load_dotenv()
api_host = os.environ.get("PATHWAY_REST_CONNECTOR_HOST", "127.0.0.1")
api_port = int(os.environ.get("PATHWAY_REST_CONNECTOR_PORT", 8080))

st.title("Healthcare Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


def upload_documents():
    uploaded_file = st.file_uploader("Upload documents (JSON Lines format)")
    if uploaded_file is not None:
        documents = list(jsonlines.Reader(uploaded_file))
        st.write(f"Uploaded {len(documents)} documents.")
        return documents
    return None


def handle_interaction():
    if prompt := st.text_input("Enter your query or message:"):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        url = f"http://{api_host}:{api_port}/"
        data = {"query": prompt, "user": "user"}

        response = requests.post(url, json=data)

        if response.status_code == 200:
            response = response.json()
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.error(f"Failed to send data. Status code: {response.status_code}")


st.sidebar.title("Options")
option = st.sidebar.radio("Choose an option:", ("Upload Documents", "Text Input"))

if option == "Upload Documents":
    documents = upload_documents()
    if documents:
        st.write("Proceed with chat interaction:")
        handle_interaction()
    else:
        st.write("Please upload documents to proceed with chat interaction.")
elif option == "Text Input":
    handle_interaction()
