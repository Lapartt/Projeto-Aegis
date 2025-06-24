# Aegis - Offline Survival Chatbot

## Objective
Aegis is an offline-first AI chatbot designed to provide assistance in survival scenarios or any situation where internet access is unavailable. It leverages a local language model and a knowledge base built from user-provided documents (PDFs, Markdown files) to answer questions and provide information. The primary goal is to run effectively on low-power, readily available hardware.

## Features
*   **Offline Operation:** Designed to work entirely without an internet connection.
*   **Local LLM:** Uses GPT4All for natural language understanding and generation.
*   **Local Knowledge Base:** Employs SQLite with FTS5 for efficient full-text search of ingested documents.
*   **CLI Interface:** Interacts with the user through a command-line interface.
*   **Voice Interaction (Conceptual):** Includes a placeholder for future voice input (STT) and output (TTS) capabilities.

## Project Structure
*   `aegis/`: Main project directory.
    *   `aegis.py`: The main chatbot application script. Handles user interaction, LLM querying, and database searching.
    *   `ingest.py`: Script for processing source documents (PDF, MD) and populating the SQLite knowledge base.
    *   `requirements.txt`: Lists Python dependencies.
    *   `README.md`: This file.
    *   `data/`: Directory for user-provided data.
        *   `data/raw/`: Place PDF and Markdown files here for ingestion.
    *   `models/`: Directory to store the GPT4All language model file.
    *   `aegis.db`: SQLite database file created by `ingest.py` (located within the `aegis/` directory).

## Installation
1.  **Clone the Repository:**
    ```bash
    # Assuming the project is hosted on Git
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Dependencies:**
    Ensure you have Python 3.x installed. Then, install the required packages:
    ```bash
    pip install -r aegis/requirements.txt
    ```

3.  **Download a GPT4All Model:**
    *   Download a GGUF-compatible GPT4All model. A good starting point is the official GPT4All website: [https://gpt4all.io/index.html](https://gpt4all.io/index.html). Look for models like "GPT4All-Falcon," "Mistral OpenOrca," or other compatible `.gguf` files.
    *   Place the downloaded model file into the `aegis/models/` directory.
    *   Rename the model file to `gpt4all-model.gguf`.

4.  **Prepare Data and Run Ingestion:**
    *   Place your PDF and/or Markdown documents into the `aegis/data/raw/` directory.
    *   Run the ingestion script to build the knowledge base:
        ```bash
        python aegis/ingest.py
        ```
        This will create or update the `aegis.db` file within the `aegis/` directory.

## Usage
1.  **Run the Chatbot:**
    ```bash
    python aegis/aegis.py
    ```

2.  **Voice Interaction (Conceptual):**
    To simulate voice mode activation (note: actual voice processing is not yet implemented):
    ```bash
    python aegis/aegis.py --voice
    ```

3.  **Example Interaction:**
    Once the chatbot is running, you can ask questions based on the documents you ingested:
    ```
    You: How do I build a shelter?
    Aegis: Thinking...
    Aegis: Based on the provided documents, to build a shelter you should...
    ```
    Type `exit` to quit the application.

## Data Ingestion
*   The Aegis system builds its knowledge from PDF (`.pdf`) and Markdown (`.md`) files.
*   Place any documents you want Aegis to learn from into the `aegis/data/raw/` directory.
*   After adding or updating files in `aegis/data/raw/`, run the ingestion script to update the local database:
    ```bash
    python aegis/ingest.py
    ```
    This script extracts text, splits it into manageable paragraphs, and stores them in the `aegis.db` SQLite database, making them searchable.

## Resource Consumption (Expected Target)
Aegis is designed with low resource consumption in mind:
*   **RAM:** Target < 4 GB during operation.
*   **CPU:** Expected to run efficiently on processors like a Ryzen 5600 (approx. 25W TDP) or similar low-power CPUs. Performance will vary based on the specific model and hardware.

This project aims to provide a useful AI tool for offline environments, prioritizing accessibility and resource efficiency.
