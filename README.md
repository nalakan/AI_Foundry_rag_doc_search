# AI_Foundry_rag_doc_search

RAG-based intelligent document search using Azure AI Foundry/Search

## Overview

**AI_Foundry_rag_doc_search** is a Retrieval-Augmented Generation (RAG) application that enables intelligent searching across uploaded documents. Powered by Azure AI Foundry and Azure Cognitive Search, the app uses advanced language models to answer questions on your document collection, providing context-aware responses through a Streamlit web interface.

---

## Features

- **Streamlit UI:** Simple and interactive chat interface for asking document-related questions.
- **Azure AI Integration:** Connects to Azure AI Foundry and Azure Cognitive Search for secure, scalable document indexing and retrieval.
- **RAG Workflow:** Combines retrieval from indexed documents with generative AI (GPT-4.1-mini) for accurate answers.
- **Session Management:** Maintains chat history per session for context and continuity.
- **Status & Debugging:** Shows agent/thread info, processing status, and supports agent/chat resets.

---

## Architecture & Flow

1. **Initialization**
   - Loads Azure credentials and configuration from environment variables.
   - Configures Streamlit layout and styling.

2. **Agent & Search Setup**
   - Authenticates with Azure using provided credentials.
   - Connects to a specified Azure Cognitive Search index (`rag-1754502262882`).
   - Initializes the AI agent (GPT-4.1-mini) with instructions to leverage document search.
   - Sets up a conversation thread for the chat session.

3. **User Query Handling**
   - Users submit queries via the chat interface.
   - The agent uses Azure AI Search to retrieve relevant document context.
   - The LLM (GPT-4.1-mini) generates a response based on retrieved context and chat history.
   - Responses are displayed alongside user messages in the chat UI.

4. **Error Handling & Controls**
   - Immediate feedback if environment variables or connections are missing.
   - Controls for clearing chat, resetting the agent, and displaying debug info.

---

## Technologies Used

- **Python**: Backend scripting and logic.
- **Streamlit**: Fast web UI/app framework.
- **Azure AI SDKs**: 
  - `azure.ai.projects`, `azure.ai.agents.models`, `azure.identity`
- **dotenv**: Loads environment variables from `.env` files.
- **Azure Cognitive Search**: Document indexing and retrieval.
- **GPT-4.1-mini**: Language model for generative answers.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Azure subscription with AI Foundry and Cognitive Search resources
- API credentials (Tenant ID, Client ID, Client Secret, Project Endpoint)
- Required Python packages (see below)

### Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/nalakan/AI_Foundry_rag_doc_search.git
   cd AI_Foundry_rag_doc_search
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Create an `.env` file or use the provided `api_settings.env`
   - Add:
     ```
     TENANT_ID=your-tenant-id
     CLIENT_ID=your-client-id
     CLIENT_SECRET=your-client-secret
     PROJECT_ENDPOINT=https://your-project-endpoint
     ```

4. **Run the Streamlit app**
   ```sh
   streamlit run streamlit-RAG_Based_AI.py
   ```

---

## Usage

1. Upload documents to your Azure AI Foundry project (MS Fabric files section).
2. Ask questions via the Streamlit chat UI.
3. The agent retrieves relevant content from your documents using Azure AI Search and responds with context-rich, generative answers.

---

## File Structure

- `streamlit-RAG_Based_AI.py` — Main Streamlit app and workflow logic.
- `api_settings.env` — Example environment variable file (not versioned for security).
- `README.md` — Project documentation (this file).
- `LICENSE` — MIT License.

---

## License

MIT License © 2025 Nalaka Wanniarachchi

---

## Troubleshooting

- **Missing Environment Variables:** Ensure all required credentials are set.
- **Azure Connection Issues:** Verify resource access and configuration.
- **Model/Agent Errors:** Check subscription limits and resource availability.

---

## Contributing

Pull requests and issues are welcome! Please open an issue to discuss major changes before submitting.

---

## Contact

For questions, reach out via GitHub Issues or contact the repository owner.
