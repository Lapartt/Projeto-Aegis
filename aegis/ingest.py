import os
import sqlite3
from pypdf import PdfReader
from markdown import markdown
from bs4 import BeautifulSoup

# Placeholder for PDF model download path (if any specific model is needed by pypdf, though it's usually self-contained)
# Placeholder for markdown model or specific setup (if any)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_md(md_path):
    """Extracts text from a Markdown file."""
    text = ""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html = markdown(md_content)
        soup = BeautifulSoup(html, 'html.parser')
        # Use a separator that's unlikely to be in the text, then split by it.
        # Or, more simply, try to preserve paragraph breaks.
        # BeautifulSoup's get_text() by default joins with '', let's try a specific separator.
        text = soup.get_text(separator='\n\n')
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {md_path}")
    except Exception as e:
        print(f"Error reading Markdown {md_path}: {e}")
    return text

def main():
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, 'aegis.db')
    # Corrected data_dir to point to 'aegis/data/raw' relative to the script's directory
    data_dir = os.path.join(script_dir, 'data', 'raw')

    conn = None  # Initialize conn to None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs (
            id INTEGER PRIMARY KEY,
            source TEXT,
            content TEXT
        )
        ''')

        cursor.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
            content,
            tokenize = "porter",
            content_rowid='id'
        )
        ''')

        # Ensure data_dir exists before trying to list its contents
        if not os.path.exists(data_dir):
            print(f"Data directory {data_dir} not found. Creating it.")
            os.makedirs(data_dir, exist_ok=True) # exist_ok=True handles concurrent creation

        if not os.listdir(data_dir):
            print(f"Data directory {data_dir} is empty. No files to process.")


        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)
            extracted_text = ""
            if filename.lower().endswith('.pdf'):
                print(f"Processing PDF: {file_path}")
                extracted_text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith('.md'):
                print(f"Processing Markdown: {file_path}")
                extracted_text = extract_text_from_md(file_path)
            else:
                print(f"Skipping unsupported file type: {filename}")
                continue

            if extracted_text:
                # Split by two or more newlines to define paragraphs
                paragraphs = [p.strip() for p in extracted_text.split('\n\n') if p.strip()]
                for para_content in paragraphs:
                    if para_content: # Ensure paragraph is not empty after stripping
                        cursor.execute("INSERT INTO docs (source, content) VALUES (?, ?)", (filename, para_content))
                        last_row_id = cursor.lastrowid
                        cursor.execute("INSERT INTO docs_fts (rowid, content) VALUES (?, ?)", (last_row_id, para_content))

        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print(f"Database connection to {db_path} closed.")

if __name__ == '__main__':
    main()
