import os
import requests
import sqlite3
import duckdb
from PIL import Image
import markdown
import subprocess

# B1 & B2: Security Checks
def B12(filepath: str) -> bool:
    """
    Ensure that the filepath is within the /data directory.
    Raises PermissionError if the filepath is outside /data.
    """
    if not filepath.startswith('/data'):
        raise PermissionError("Access outside /data is not allowed.")
    return True

# B3: Fetch Data from an API
def B3(url: str, save_path: str) -> None:
    """
    Fetch data from a URL and save it to the specified path.
    """
    if not B12(save_path):
        return None
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and Make a Commit
def B4(repo_url: str, commit_message: str) -> None:
    """
    Clone a Git repository and make a commit.
    """
    repo_path = "/data/repo"
    if not B12(repo_path):
        return None
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)
    subprocess.run(["git", "-C", repo_path, "add", "."], check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", commit_message], check=True)

# B5: Run SQL Query
def B5(db_path: str, query: str, output_filename: str) -> list:
    """
    Execute a SQL query on a SQLite or DuckDB database and save the result to a file.
    """
    if not B12(db_path) or not B12(output_filename):
        return None
    conn = sqlite3.connect(db_path) if db_path.endswith('.db') else duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Web Scraping
def B6(url: str, output_filename: str) -> None:
    """
    Scrape data from a website and save it to a file.
    """
    if not B12(output_filename):
        return None
    response = requests.get(url)
    with open(output_filename, 'w') as file:
        file.write(response.text)

# B7: Image Processing
def B7(image_path: str, output_path: str, resize: tuple = None) -> None:
    """
    Compress or resize an image and save it to the specified path.
    """
    if not B12(image_path) or not B12(output_path):
        return None
    img = Image.open(image_path)
    if resize:
        img = img.resize(resize)
    img.save(output_path)

# B8: Audio Transcription
def B8(audio_path: str) -> str:
    """
    Transcribe audio from an MP3 file using OpenAI's Whisper API.
    """
    if not B12(audio_path):
        return None
    import openai
    openai.api_key = os.environ["AIPROXY_TOKEN"]
    with open(audio_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
    return transcription['text']

# B9: Markdown to HTML Conversion
def B9(md_path: str, output_path: str) -> None:
    """
    Convert a Markdown file to HTML and save it to the specified path.
    """
    if not B12(md_path) or not B12(output_path):
        return None
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

# B10: API Endpoint for CSV Filtering
def B10(csv_path: str, filter_column: str, filter_value: str) -> list:
    """
    Filter a CSV file based on a column and value, and return the result as JSON.
    """
    if not B12(csv_path):
        return None
    import pandas as pd
    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]
    return filtered.to_dict(orient='records')