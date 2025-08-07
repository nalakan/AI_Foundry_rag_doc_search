import os
import streamlit as st
from azure.ai.projects import AIProjectClient
from azure.identity import ClientSecretCredential
from azure.ai.agents.models import AzureAISearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv('C:\\Users\\nalak\\Documents\\RnD\\AIFOUNDRY_AGents\\RAG after GA codebased using joys stuff\\STREAMLIT-APP\\api_settings.env')

# --- Validate environment variables ---
try:
    TENANT_ID = os.getenv("TENANT_ID")
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
    
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, PROJECT_ENDPOINT]):
        raise ValueError("Missing one or more required environment variables.")
except Exception as e:
    st.error(f"Error loading environment variables: {e}")
    st.stop()

# Streamlit layout config
st.set_page_config(page_title="RAG-Based Intelligent Document Search", layout="wide")

# Simple, minimal styling that won't interfere with inputs
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        color: #000000;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #4CAF50 !important;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        color: #000000;
    }
    .agent-message {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        color: #000000;
        border-left: 4px solid #4CAF50;
    }
    .stFormSubmitButton > button {
        width: 100px;
        margin-top: 5px !important;
    }
    .stTextInput > div > div > input:disabled {
        background-color: #e0e0e0 !important;
        color: #000000 !important;
        cursor: not-allowed !important;
        border: 2px solid #cccccc !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🤖🧠 RAG-Based Intelligent Document Search")
st.write("🔍 Ask me anything on your docs using the next level search capabilities!")

# --- Session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

if "agent_config" not in st.session_state:
    try:
        # Create project client
        credential = ClientSecretCredential(
            tenant_id=TENANT_ID,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )

        project_client = AIProjectClient(
            credential=credential,
            endpoint=PROJECT_ENDPOINT
        )

        # Find ragaisearch002 connection
        conn_list = list(project_client.connections.list())
        ragaisearch002_conn = None
        for conn in conn_list:
            if conn.get("name", "") == "ragaisearch002":
                ragaisearch002_conn = conn
                break
        
        if not ragaisearch002_conn:
            st.error("❌ AI Search connection not found!")
            st.stop()
        
        conn_id = ragaisearch002_conn['id']
        st.success("✅ Connected to AI Search")

        # Initialize AI search tool
        ai_search = AzureAISearchTool(
            index_connection_id=conn_id, 
            index_name="rag-1754502262882"
        )

        # Create the AI agent
        agent = project_client.agents.create_agent(
            model="gpt-4.1-mini",
            name="simple-agent",
            instructions="You are a helpful RAG based AI assistant. Provide clear, concise responses based on the azure AI search where files are uploaded in MS Fabric files section.so when user asked about the uploaded docs you are getting context from AI search and embedding models",
            tools=ai_search.definitions,
            tool_resources=ai_search.resources,
        )

        # Create a conversation thread
        thread = project_client.agents.threads.create()

        st.session_state.agent_config = {
            "agent_id": agent.id,
            "thread_id": thread.id,
            "project_client": project_client,
        }
        
        st.success("✅ Agent ready!")
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

# --- Display Chat History ---
st.subheader("💬 Conversation")

for i, (role, message) in enumerate(st.session_state.chat_history):
    if role == "User":
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-message"><strong>Assistant:</strong> {message}</div>', unsafe_allow_html=True)

# --- Input Section ---
st.subheader("✏️ Your Message")

# Only show input form when not processing
if not st.session_state.is_processing:
    # Use form to make input more reliable
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Enter your message:", 
            placeholder="Type your question here...",
            help="Ask me anything!",
            label_visibility="collapsed"
        )
        
        # Place send button below the input field
        send_button = st.form_submit_button("Send 📤")
else:
    # Show disabled input when processing - display what user typed
    if "current_user_input" in st.session_state:
        st.text_input(
            "Enter your message:", 
            value=st.session_state.current_user_input,
            label_visibility="collapsed",
            disabled=True,
            key=f"disabled_input_{len(st.session_state.chat_history)}"
        )
    else:
        st.text_input(
            "Enter your message:", 
            placeholder="Processing...",
            label_visibility="collapsed",
            disabled=True,
            key=f"disabled_empty_{len(st.session_state.chat_history)}"
        )
    send_button = False

# --- Message Processing ---
if send_button and user_input and not st.session_state.is_processing:
    # Set processing state to True immediately
    st.session_state.is_processing = True
    st.session_state.current_user_input = user_input
    st.rerun()

# Handle the actual processing when in processing state
if st.session_state.is_processing and "current_user_input" in st.session_state:
    # Show the thinking message
    st.info("🤔 AI is thinking... Please wait for the response.")
    
    try:
        project_client = st.session_state.agent_config["project_client"]
        thread_id = st.session_state.agent_config["thread_id"]
        agent_id = st.session_state.agent_config["agent_id"]
        
        user_msg = st.session_state.current_user_input

        # Send message
        project_client.agents.messages.create(
            thread_id=thread_id, 
            role="user", 
            content=user_msg
        )
        
        # Get response
        run = project_client.agents.runs.create_and_process(
            thread_id=thread_id, 
            agent_id=agent_id
        )

        if run.status == "failed":
            response_text = f"❌ Error: {run.last_error}"
        else:
            messages = project_client.agents.messages.list(
                thread_id=thread_id, 
                order="desc", 
                limit=1
            )
            
            response_text = "No response received."
            messages_list = list(messages)
            if messages_list:
                latest_message = messages_list[0]
                if latest_message.role == "assistant" and latest_message.content:
                    try:
                        if hasattr(latest_message.content[0], 'text'):
                            response_text = latest_message.content[0].text.value
                        else:
                            response_text = str(latest_message.content[0])
                    except:
                        response_text = "Could not parse response."

        # Add both messages to chat history
        st.session_state.chat_history.append(("User", user_msg))
        st.session_state.chat_history.append(("Agent", response_text))
        
        # Reset processing state
        st.session_state.is_processing = False
        del st.session_state.current_user_input
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error: {e}")
        if "current_user_input" in st.session_state:
            user_msg = st.session_state.current_user_input
            st.session_state.chat_history.append(("User", user_msg))
        st.session_state.chat_history.append(("Agent", f"Error: {str(e)}"))
        
        # Reset processing state
        st.session_state.is_processing = False
        if "current_user_input" in st.session_state:
            del st.session_state.current_user_input
        st.rerun()

# --- Sidebar Controls ---
with st.sidebar:
    st.header("🛠️ Controls")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state.is_processing = False
        st.rerun()
    
    if st.button("🔄 Reset Agent"):
        if "agent_config" in st.session_state:
            try:
                project_client = st.session_state.agent_config["project_client"]
                agent_id = st.session_state.agent_config["agent_id"]
                project_client.agents.delete_agent(agent_id)
            except:
                pass
        
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.write("---")
    status = "Processing..." if st.session_state.is_processing else ("Ready" if "agent_config" in st.session_state else "Initializing...")
    st.write(f"**Status:** {status}")

# Show current state for debugging
if st.checkbox("🔍 Show Debug Info"):
    st.write("**Chat History Length:**", len(st.session_state.chat_history))
    st.write("**Is Processing:**", st.session_state.is_processing)
    if "agent_config" in st.session_state:
        st.write("**Agent ID:**", st.session_state.agent_config["agent_id"][:20] + "...")
        st.write("**Thread ID:**", st.session_state.agent_config["thread_id"][:20] + "...")