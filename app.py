import streamlit as st
import os
import sys
import shutil
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from models.llm import get_llm
from config import config
from utils.rag_utils import load_and_split_document, create_vector_store, get_retriever
from utils.search_utils import perform_web_search

# Ensure temp directory exists
if not os.path.exists("temp"):
    os.makedirs("temp")

def get_chat_response(chat_model, messages, system_prompt, context=""):
    """Get response from the chat model"""
    try:
        # Prepare messages for the model
        final_system_prompt = system_prompt
        if context:
            final_system_prompt += f"\n\nCONTEXT FROM DOCUMENTS/SEARCH:\n{context}"
            
        formatted_messages = [SystemMessage(content=final_system_prompt)]
        
        # Add conversation history
        for msg in messages:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))
        
        # Get response from model
        response = chat_model.invoke(formatted_messages)
        return response.content
    
    except Exception as e:
        return f"Error getting response: {str(e)}"

def instructions_page():
    """Instructions and setup page"""
    st.title("The Chatbot Blueprint")
    st.markdown("Welcome! Follow these instructions to set up and use the chatbot.")
    
    st.markdown("""
    ## 🔧 Installation
                
    
    First, install the required dependencies:
    
    ```bash
    pip install -r requirements.txt
    ```
    
    ## API Key Setup
    
    You'll need API keys from your chosen provider. Get them from:
    
    ### Groq (Free Tier Available)
    - Visit [Groq Console](https://console.groq.com/keys)
    - Create a new API key
    - Set the variables in config/config.py
    
    ### Google Gemini (Free Tier Available)
    - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Create a new API key
    - Set the variables in config/config.py
    - Default model: **gemini-2.5-flash**
    
    ### OpenAI (Paid)
    - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
    - Create a new API key
    - Set the variables in config/config.py or enter it in the app
    
    ## How to Use
    
    1. **Select a Model Provider**: Choose between Groq, Google, or OpenAI.
    2. **Choose a Data Source**:
        - **Chat Only**: Standard conversational AI.
        - **RAG (Document)**: Upload a PDF/TXT to ask questions about it.
        - **Web Search**: Search the internet for real-time info.
    3. **Select Response Mode**: Concise for summaries, Detailed for deep dives.
    4. **Start chatting**!
    
    ## Tips
    
    - **System Prompts**: Customize the AI's personality and behavior
    - **Model Selection**: Different models have different capabilities and costs
    - **API Keys**: Can be entered in the app or set as environment variables
    - **Chat History**: Persists during your session but resets when you refresh
    
    ## Troubleshooting
    
    - **API Key Issues**: Make sure your API key is valid and has sufficient credits
    - **Model Not Found**: Check the provider's documentation for correct model names
    - **Connection Errors**: Verify your internet connection and API service status
    
    ---
    
    Ready to start chatting? Navigate to the **Chat** page using the sidebar! 
    """)

def chat_page():
    """Main chat interface page"""
    st.title(config.APP_TITLE)
    st.caption(f"{config.APP_ICON} Powered by LangChain & Streamlit")
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Model Selection
        provider = st.selectbox("Select Provider", ["groq", "google", "openai"], index=0)
        
        # OpenAI API Key Input
        openai_api_key = None
        if provider == "openai":
            st.warning("⚠️ **Note:** OpenAI is not free. Please use your API Key to continue, or switch to Gemini or Groq for free alternatives.")
            openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
            if not openai_api_key and not config.OPENAI_API_KEY:
                st.error("Please enter your OpenAI API Key to proceed.")
                return
        
        # Data Source Selection
        data_source = st.radio("Data Source", ["Chat Only", "RAG (Document)", "Web Search"])
        
        # Response Mode
        response_mode = st.radio("Response Mode", ["Concise", "Detailed"])
        
        # RAG File Uploader
        vector_store = None
        if data_source == "RAG (Document)":
            uploaded_file = st.file_uploader("Upload Document (PDF/TXT)", type=["pdf", "txt"])
            if uploaded_file:
                with st.spinner("Processing document..."):
                    # Save file to temp
                    file_path = os.path.join("temp", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process
                    try:
                        chunks = load_and_split_document(file_path)
                        vector_store = create_vector_store(chunks)
                        st.success("Document processed successfully!")
                        
                        # Proactive assistant prompt
                        if "messages" not in st.session_state:
                            st.session_state.messages = []
                        if not st.session_state.messages:
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": "I've processed your document. How can I help you with it? You can ask for a summary, specific details, or analysis."
                            })
                    except Exception as e:
                        st.error(f"Error processing document: {e}")
    
    # Initialize Chat Model
    try:
        if provider == "openai":
            chat_model = get_llm(provider, openai_api_key=openai_api_key)
        else:
            chat_model = get_llm(provider)
    except Exception as e:
        st.error(f"Error initializing {provider} model: {e}")
        if provider == "google":
            st.warning("⚠️ It seems your Google API Key doesn't have access to the selected Gemini model. Please check your Google Cloud Console or switch to **Groq**.")
        elif provider == "openai":
             st.warning("⚠️ Please check your OpenAI API Key credits and permissions.")
        return

    # Define System Prompt based on Mode
    base_prompt = "You are a Strategic Business Intelligence Analyst."
    if response_mode == "Concise":
        system_prompt = f"{base_prompt} Provide short, executive summaries. Focus on key metrics and high-level insights. Be brief and to the point."
    else:
        system_prompt = f"{base_prompt} Provide detailed, in-depth analysis. Explain the 'why' and 'how'. Include context, nuance, and comprehensive explanations."

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                
                context = ""
                # Handle RAG
                if data_source == "RAG (Document)" and vector_store:
                    retriever = get_retriever(vector_store)
                    docs = retriever.invoke(prompt)
                    context = "\n".join([doc.page_content for doc in docs])
                    st.info(f"Retrieved {len(docs)} relevant chunks from document.")
                
                # Handle Web Search
                elif data_source == "Web Search":
                    search_results = perform_web_search(prompt)
                    context = search_results
                    st.info("Performed web search.")
                
                response = get_chat_response(chat_model, st.session_state.messages, system_prompt, context)
                st.markdown(response)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Navigation
    with st.sidebar:
        st.title("Navigation")
        page = st.radio(
            "Go to:",
            ["Chat", "Instructions"],
            index=0
        )
        
        # Add clear chat button in sidebar for chat page
        if page == "Chat":
            st.divider()
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
    
    # Route to appropriate page
    if page == "Instructions":
        instructions_page()
    if page == "Chat":
        chat_page()

if __name__ == "__main__":
    main()