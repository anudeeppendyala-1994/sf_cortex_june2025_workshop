# 🤖 Unified Conversations — Enterprise Chatbot with Snowflake Cortex

## Quick Links
* Connect with me on [LinkedIn](https://www.linkedin.com/in/anudeep-p-283763232/)

---

## 📖 Overview
This project demonstrates a **Smart Enterprise Chatbot** built on Snowflake's **Cortex AI Services**, including **Cortex Agents**, **Semantic Models**, and **Cortex Search Service**.  

The chatbot enables employees across departments—like HR, Sales, Marketing, and Finance—to ask questions in natural language and retrieve insights seamlessly from both **structured data** (Snowflake tables) and **unstructured data** (documents, PDFs, knowledge bases).  

It showcases a unified, enterprise-ready approach for cross-functional data intelligence and self-service AI.

---

## 🗂️ Project Structure

| Type | Files | Description |
|:-----|:------|:------------|
| 📄 Sample PDFs | `HR_Policies.pdf`, `Marketing_Strategy.pdf` | Simulated unstructured content for retrieval |
| 📊 Sample Data Files | `employee_data.csv`, `sales_data.csv` | Structured departmental datasets |
| 🧐 Semantic Model YAML | `hr_semantic_model.yaml, sales_semantic_model.yaml, Marketing_semantic_model.yaml` | Definitions for Cortex Analyst semantic model |
| 🌐 Streamlit App | `streamlit_app.py` | Interactive UI for querying the chatbot |
| 📋 Documentation | `README.md` | This project guide |

---

## 🧬 Use Case Details

### 🌟 Problem Statement
Organizations often struggle to deliver **centralized, intelligent, self-service insights** when data is spread across structured databases and unstructured documents. Different teams need answers tailored to their department—HR, Sales, Marketing, Finance—all from one unified assistant.

Our chatbot bridges this gap by:
✅ Combining structured and unstructured data sources  
✅ Enabling natural language Q&A  
✅ Serving multiple departments in one interface

---

## 🧩 Solution Approach

### 1️⃣ Structured Data Insights
- Uses **Cortex Semantic Models** to define table relationships, dimensions, and measures
- Allows employees to query data warehouses using natural language
- Example: *“Show monthly sales by region.”*

### 2️⃣ Unstructured Data Insights
- Leverages **Cortex Search Service** with embeddings and parse document features
- Retrieves answers from PDFs, manuals, and policy documents
- Example: *“What is the leave policy for managers?”*

### 3️⃣ Unified Chatbot Experience
- Combines structured + unstructured capabilities in a single **Cortex Agent**
- Streamlit in Snowflake app enables an easy-to-use, enterprise-ready interface
- Supports multiple departments with customizable prompts

---

## 🧬 Snowflake Cortex Integration

### Cortex Agent
- Routes user questions to either structured data (via Semantic Model) or unstructured content (via Search Service)
- Supports department-level customization

### Cortex Analyst
- Defines the **Semantic Model** for structured databases
- Improves natural language understanding of organizational metrics

### Cortex Search Service
- Parses and embeds unstructured content for semantic retrieval
- Supports rich text, PDFs, knowledge bases

---

## 🚀 How to Run

1. **Snowflake Setup**:
   - Ensure Snowflake account has **Cortex** features enabled
   - Load structured CSV datasets into Snowflake tables
2. **Semantic Model**:
   - Create and deploy the Semantic Model YAML
3. **Cortex Agent**:
   - Run SQL setup scripts to register and configure the Agent
4. **Cortex Search**:
   - Upload PDFs and docs to Snowflake stages
   - Create and train the Cortex Search Service
5. **App UI**:
   - Deploy `enterprise_chatbot_app.py` as a Streamlit in Snowflake app
   - Provide end-users with the unified chatbot interface

---

## 🌟 Highlights

- Supports **multiple departments** with a single assistant
- Unified natural language interface for **structured + unstructured** data
- Snowflake-native solution with Cortex integration
- Demo-ready with GitHub notebooks and sample datasets
- Fully self-service architecture with Streamlit in Snowflake


---

# 💼 Built for Enterprise Intelligence, Powered by Snowflake Cortex 🚀
