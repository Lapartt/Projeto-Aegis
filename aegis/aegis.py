import argparse
import sqlite3
import os # Added for checking model file existence
from gpt4all import GPT4All # Assuming gpt4all is installed

# Placeholder for PocketSphinx and eSpeak imports if they were to be used

def main():
    parser = argparse.ArgumentParser(description="Aegis AI Assistant")
    parser.add_argument('--voice', action='store_true', help='Enable voice input/output (placeholder)')
    args = parser.parse_args()

    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, 'aegis.db')
    model_path = os.path.join(script_dir, 'models', 'gpt4all-model.gguf')

    # Model Loading
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        print("Please download the GPT4All model (e.g., 'ggml-gpt4all-j-v1.3-groovy.bin')")
        print("and place it at the specified path, renaming it to 'gpt4all-model.gguf'.")
        print("Alternatively, update the 'model_path' variable in the script.")
        exit(1)

    print(f"Loading model from: {model_path}")
    try:
        model = GPT4All(model_path)
    except Exception as e:
        print(f"Error loading GPT4All model: {e}")
        print("Ensure the model file is a valid GGUF format and compatible with your gpt4all library version.")
        exit(1)

    # Voice Input/Output (Placeholder)
    if args.voice:
        print("Voice mode activated (PocketSphinx STT and eSpeak TTS would be used here).")

    print("Aegis AI Assistant. Type 'exit' to quit.")
    while True:
        try:
            user_q = input("You: ")
        except EOFError: # Handle EOF if input is redirected
            print("\nExiting due to EOF.")
            break

        if user_q.lower() == 'exit':
            break

        # Database Search
        conn = None # Initialize conn
        results = []
        try:
            if not os.path.exists(db_path):
                print(f"Error: Database file {db_path} not found. Please run ingest.py first.")
                continue # Skip to next iteration of the loop

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            # Using a try-except for the query in case docs_fts doesn't exist or is empty
            try:
                cursor.execute('''
                SELECT content FROM docs_fts
                WHERE docs_fts MATCH :query
                ORDER BY rank LIMIT 5;
                ''', {'query': user_q})
                results = cursor.fetchall()
            except sqlite3.OperationalError as oe:
                if "no such table: docs_fts" in str(oe):
                    print(f"Warning: Table 'docs_fts' not found in {db_path}. Did you run ingest.py?")
                elif "unable to use function MATCH" in str(oe):
                     print(f"Warning: FTS5 MATCH not working as expected on 'docs_fts' in {db_path}. Is the table populated correctly?")
                else:
                    print(f"Database query error: {oe}")
                results = [] # Ensure results is empty on error

        except sqlite3.Error as e:
            print(f"Database connection or query error: {e}")
            results = [] # Ensure results is empty on error
        finally:
            if conn:
                conn.close()

        # Prompt Construction
        context_str_header = "Contexto:"
        if results:
            context_items = []
            for i, row in enumerate(results):
                context_items.append(f"{i+1}) {row[0]}")
            context_str_content = "\n".join(context_items)
            context_str = f"{context_str_header}\n{context_str_content}"
        else:
            context_str = f"{context_str_header} Nenhum documento relevante encontrado."

        full_prompt = f"{context_str}\n\nPergunta: {user_q}\n\nResposta:"

        # Generate Response (GPT4All)
        print("Aegis: Thinking...") #thinking message
        try:
            response_generator = model.generate(full_prompt, max_tokens=200, streaming=False)
            # Assuming response_generator yields tokens or a full response.
            # For non-streaming, it's often a direct string.
            # If it's a generator, iterate: response = "".join(list(response_generator))
            # Based on gpt4all docs, generate() returns a string directly if streaming=False
            response = response_generator
            if isinstance(response, dict) and 'choices' in response: # Handle more complex response structures if any
                 response = response['choices'][0].get('text', 'No text in response choice.')

        except Exception as e:
            response = f"Error generating response: {e}"

        print(f"Aegis: {response}")

    print("Aegis: Goodbye!")

if __name__ == '__main__':
    main()
