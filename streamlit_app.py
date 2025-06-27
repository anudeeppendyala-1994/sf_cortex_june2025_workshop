# chatbot_app.py
# Smart Enterprise Chatbot for HR, Sales, and Marketing (June 2025 version)
# Uses new Snowflake databases, tables, and Cortex search service as per BUILD_AGENTS_FOR_ENTERPRISE.ipynb
import streamlit as st
import json
import _snowflake
from snowflake.snowpark.context import get_active_session
import time

# Initialize session state
if "selected_department" not in st.session_state:
    st.session_state.selected_department = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session" not in st.session_state:
    try:
        st.session_state.session = get_active_session()
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {str(e)}")
        st.stop()

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .welcome-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        color: #1E88E5;
    }
    .company-name {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .company-tagline {
        font-size: 1em;
        color: #666;
    }
    .department-button {
        width: 100px;
        padding: 8px;
        margin: 5px;
        border-radius: 5px;
        border: none;
        font-size: 0.9em;
        font-weight: normal;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        text-align: center;
    }
    .department-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .chat-container {
        background: white;
        border-radius: 5px;
        padding: 10px;
        margin-top: 10px;
    }
    .department-header {
        text-align: center;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
        color: white;
        font-size: 1.2em;
    }
    .error-message {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
        border-radius: 5px;
        padding: 10px;
        margin: 5px 0;
        color: #c62828;
        font-size: 0.9em;
    }
    .stButton button {
        width: 100px;
        padding: 5px 10px;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

API_ENDPOINT = "/api/v2/cortex/agent:run"
API_TIMEOUT = 50000  # in milliseconds

# Department-specific configurations (updated for new DB/Schema/Table names)
DEPARTMENT_CONFIGS = {
    "HR": {
        "search_service": "ENTERPRISE_DATA_DB.ENTERPRISE_DATA_SCHEMA.DOCUMENT_SEARCH_SERVICE",
        "semantic_model": "@ENTERPRISE_DATA_DB.ENTERPRISE_DATA_SCHEMA.landing_stg/Semantic_models/HR/hr_semantic_model.yaml",  # Not used in this version, but placeholder if needed
        "avatar": "👥",
        "greeting": "Hello HR Professional, how can I assist you today?",
        "tables": [
            "HR_DB.RAW.EMPLOYEES",
            "HR_DB.RAW.DEPARTMENTS",
            "HR_DB.RAW.PERFORMANCE_REVIEWS",
            "HR_DB.ANALYTICS.DEPARTMENT_STATS"
        ],
        "description": "Access employee data, department information, and performance metrics",
        "color": "#4CAF50",
        "button_color": "background-color: #4CAF50; color: white;"
    },
    "Sales": {
        "search_service": "ENTERPRISE_DATA_DB.ENTERPRISE_DATA_SCHEMA.DOCUMENT_SEARCH_SERVICE",
        "semantic_model": "@ENTERPRISE_DATA_DB.ENTERPRISE_DATA_SCHEMA.landing_stg/Semantic_models/Sales/sales_semantic_model.yaml",
        "avatar": "💰",
        "greeting": "Hello Sales Professional, how can I assist you today?",
        "tables": [
            "SALES_DB.RAW.SALES_TRANSACTIONS",
            "SALES_DB.RAW.CUSTOMERS",
            "SALES_DB.RAW.PRODUCTS",
            "SALES_DB.ANALYTICS.SALES_PERFORMANCE"
        ],
        "description": "Analyze sales performance, customer data, and product metrics",
        "color": "#2196F3",
        "button_color": "background-color: #2196F3; color: white;"
    },
    "Marketing": {
        "search_service": "ENTERPRISE_DATA_DB.ENTERPRISE_DATA_SCHEMA.DOCUMENT_SEARCH_SERVICE",
        "semantic_model": "@ENTERPRISE_DATA_DB.ENTERPRISE_DATA_SCHEMA.landing_stg/Semantic_models/Marketing/marketing_semantic_model.yaml",
        "avatar": "📢",
        "greeting": "Hello Marketing Professional, how can I assist you today?",
        "tables": [
            "MARKETING_DB.RAW.CAMPAIGNS",
            "MARKETING_DB.RAW.CAMPAIGN_METRICS",
            "MARKETING_DB.ANALYTICS.CAMPAIGN_PERFORMANCE"
        ],
        "description": "Track campaign performance, marketing metrics, and ROI analysis",
        "color": "#9C27B0",
        "button_color": "background-color: #9C27B0; color: white;"
    }
}

def run_snowflake_query(query):
    try:
        # Add error handling for specific tables
        if "EMPLOYEES" in query and "HR_DB" not in query:
            st.warning("Please specify the HR_DB database when querying employee data")
            return None
        if "SALES_TRANSACTIONS" in query and "SALES_DB" not in query:
            st.warning("Please specify the SALES_DB database when querying sales data")
            return None
        if "CAMPAIGNS" in query and "MARKETING_DB" not in query:
            st.warning("Please specify the MARKETING_DB database when querying campaign data")
            return None
        if "@" in query and "landing_stg" not in query:
            query = query.replace("@", "@landing_stg/")
        df = st.session_state.session.sql(query.replace(";", ""))
        return df
    except Exception as e:
        st.error(f"Error executing SQL: {str(e)}")
        return None

def snowflake_api_call(query: str, department: str, limit: int = 10):
    config = DEPARTMENT_CONFIGS[department]
    # Keywords that suggest database queries
    db_keywords = [
        'performance', 'metrics', 'data', 'report', 'statistics',
        'campaign', 'sales', 'revenue', 'transactions', 'customers',
        'employees', 'budget', 'cost', 'analytics', 'kpi',
        'salary', 'department', 'position', 'hire date', 'manager',
        'product', 'category', 'price', 'region', 'channel',
        'impressions', 'clicks', 'conversions', 'spend', 'roi','org', 'organization'
    ]
    # Keywords that suggest PDF/document search
    pdf_keywords = [
        'document', 'policy', 'procedure', 'guide', 'manual',
        'process', 'strategy', 'plan', 'framework', 'template',
        'pdf', 'file', 'content', 'information', 'details'
    ]
    is_db_query = any(keyword in query.lower() for keyword in db_keywords)
    is_pdf_query = any(keyword in query.lower() for keyword in pdf_keywords)
    tools = []
    tool_resources = {}
    if is_db_query:
        tools.append({"tool_spec": {"type": "cortex_analyst_text_to_sql", "name": "analyst1"}})
        if config["semantic_model"]:
            tool_resources["analyst1"] = {"semantic_model_file": config["semantic_model"]}
    if is_pdf_query or not is_db_query:
        tools.append({"tool_spec": {"type": "cortex_search", "name": "search1"}})
        tool_resources["search1"] = {
            "name": config["search_service"],
            "max_results": limit,
            "id_column": "CHUNK",
            "filter": {"@eq": {"DEPARTMENT": department.upper()}}
        }
    payload = {
        "model": "claude-3-5-sonnet",
        "response-instruction": f"""You will always maintain a professional tone and provide a concise response, you will always refer the user as {department} Professional. \nIf the query is about data or metrics, always use the database tables: {', '.join(config['tables'])}. \nIf the query is about policies, procedures, or general information, use the document search.\nFor data queries, always include relevant metrics and percentages where applicable.\nFormat numbers with appropriate separators and decimal places.\nFor time-based queries, always specify the time period in the response.""",
        "messages": [{"role": "user", "content": [{"type": "text", "text": query}]}],
        "tools": tools,
        "tool_resources": tool_resources,
    }
    try:
        resp = _snowflake.send_snow_api_request(
            "POST",
            API_ENDPOINT,
            {},
            {},
            payload,
            None,
            API_TIMEOUT,
        )
        if resp["status"] != 200:
            st.error(f"❌ HTTP Error: {resp['status']} - {resp.get('reason', 'Unknown reason')}")
            st.error(f"Response details: {resp}")
            return None
        try:
            response_content = json.loads(resp["content"])
        except json.JSONDecodeError:
            st.error("❌ Failed to parse API response. The server may have returned an invalid JSON format.")
            st.error(f"Raw response: {resp['content'][:200]}...")
            return None
        return response_content
    except Exception as e:
        st.error(f"Error making request: {str(e)}")
        return None

def process_sse_response(response):
    text = ""
    sql = ""
    citations = []
    if not response or isinstance(response, str):
        return text, sql, citations
    try:
        for event in response:
            if event.get("event") == "message.delta":
                data = event.get("data", {})
                delta = data.get("delta", {})
                for content_item in delta.get("content", []):
                    content_type = content_item.get("type")
                    if content_type == "tool_results":
                        tool_results = content_item.get("tool_results", {})
                        if "content" in tool_results:
                            for result in tool_results["content"]:
                                if result.get("type") == "json":
                                    text += result.get("json", {}).get("text", "")
                                    search_results = result.get("json", {}).get("searchResults", [])
                                    for search_result in search_results:
                                        citations.append({
                                            "source_id": search_result.get("source_id", ""),
                                            "doc_id": search_result.get("doc_id", ""),
                                        })
                                    sql = result.get("json", {}).get("sql", "")
                    if content_type == "text":
                        text += content_item.get("text", "")
    except Exception as e:
        st.error(f"Error processing events: {str(e)}")
    return text, sql, citations

def main():
    st.markdown("""
        <div class="welcome-header">
            <div class="company-name">Cortex AI Assistant</div>
            <div class="company-tagline">Your Enterprise Co-Pilot for HR, Sales, and Marketing</div>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.selected_department is None:
        st.markdown("<h3 style='text-align: center;'>Choose your functional area to begin</h3>", unsafe_allow_html=True)
        
        cols = st.columns(len(DEPARTMENT_CONFIGS))
        for idx, (dept, config) in enumerate(DEPARTMENT_CONFIGS.items()):
            with cols[idx]:
                container = st.container(border=True)
                container.markdown(f"<div style='text-align: center; font-size: 3em;'>{config['avatar']}</div>", unsafe_allow_html=True)
                container.markdown(f"<h4 style='text-align: center;'>{dept}</h4>", unsafe_allow_html=True)
                container.markdown(f"<p style='text-align: center;'>{config['description']}</p>", unsafe_allow_html=True)

                if container.button("Select", key=f"btn_{dept}", use_container_width=True):
                    st.session_state.selected_department = dept
                    st.session_state.messages = [{
                        "role": "assistant",
                        "content": config["greeting"]
                    }]
                    st.rerun()
    else:
        config = DEPARTMENT_CONFIGS[st.session_state.selected_department]
        st.markdown(f"""
            <div class="department-header" style="background-color: {config['color']}">
                {config['avatar']} {st.session_state.selected_department}
            </div>
        """, unsafe_allow_html=True)
        if st.button("← Back", key="back_button"):
            st.session_state.selected_department = None
            st.session_state.messages = []
            st.rerun()
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            avatar = "👤" if message["role"] == "user" else config["avatar"]
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"].replace("•", "\n\n"))
        if query := st.chat_input("How can I help you?"):
            with st.chat_message("user", avatar="👤"):
                st.markdown(query)
            st.session_state.messages.append({"role": "user", "content": query})
            with st.spinner("Processing..."):
                try:
                    response = snowflake_api_call(query, st.session_state.selected_department, 4)
                    if response is None:
                        st.error("Failed to get response. Please try again.")
                        return
                    text, sql, citations = process_sse_response(response)
                    if text:
                        text = text.replace("【†1†】", "")
                        st.session_state.messages.append({"role": "assistant", "content": text})
                        with st.chat_message("assistant", avatar=config["avatar"]):
                            st.markdown(text.replace("•", "\n\n"))
                            if citations:
                                st.markdown("**Sources:**")
                                for i, citation in enumerate(citations):
                                    chunk = citation.get("doc_id", "")
                                    if chunk:
                                        with st.expander(f"Reference [{i+1}]"):
                                            st.markdown(chunk[:500] + "...")
                    if sql:
                        with st.chat_message("assistant", avatar=config["avatar"]):
                            st.markdown("**SQL Query:**")
                            st.code(sql, language="sql")
                            sql_results = run_snowflake_query(sql)
                            if sql_results is not None:
                                st.markdown("**Results:**")
                                st.dataframe(sql_results)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.markdown('<div class="error-message">Please try again.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
