import os
import re
import webbrowser
from pathlib import Path

import openai
from openai.types.responses import ResponseInputParam

# Set your API key directly here for testing
OPENAI_API_KEY = "your key"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_response_output_text(input: str | ResponseInputParam):
    print("[DEBUG] Sending prompt to GPT-5...")
    response = client.responses.create(
        model="gpt-5",
        input=input,
    )
    print("[DEBUG] Received response from GPT-5.")
    return response.output_text

def extract_html_from_text(text: str):
    print("[DEBUG] Extracting HTML from response...")
    html_block = re.search(r"```html\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if html_block:
        print("[DEBUG] Found HTML code block.")
        return html_block.group(1)
    any_block = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if any_block:
        print("[DEBUG] Found generic code block.")
        return any_block.group(1)
    print("[DEBUG] No code block found, using full text.")
    return text

def save_html(html: str, filename: str) -> Path:
    print(f"[DEBUG] Saving HTML to outputs/{filename} ...")
    base_dir = Path(__file__).parent
    outputs_dir = base_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    output_path = outputs_dir / filename
    output_path.write_text(html, encoding="utf-8")
    print(f"[DEBUG] Saved HTML to {output_path}")
    return output_path

def open_in_browser(path: Path) -> None:
    print(f"[DEBUG] Opening {path} in browser...")
    webbrowser.open(path.as_uri())

def make_website_and_open_in_browser(*, website_input: str | ResponseInputParam, filename: str = "website.html"):
    response_text = get_response_output_text(website_input)
    html = extract_html_from_text(response_text)
    output_path = save_html(html, filename)
    open_in_browser(output_path)

if __name__ == "__main__":
    # Example usage:
    print("[INFO] build me a website for throwing tables for fun")
    prompt = "Make me a website for throwing tables for fun."
    make_website_and_open_in_browser(website_input=prompt, filename="throwing_tables_website.html")
    print("[INFO] Done. Check the outputs folder for the generated website.")
