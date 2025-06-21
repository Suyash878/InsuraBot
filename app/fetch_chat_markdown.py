import requests
import os
import sys

def fetch_and_save_chat_markdown(chat_id, api_url="http://localhost:8000", output_dir="chat_markdowns"):
    # Fetch chat history from the API
    url = f"{api_url}/chat/{chat_id}/history"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "success":
        print(f"Error: {data.get('message')}")
        return

    # Format as markdown
    lines = [f"# Chat History for `{chat_id}`\n"]
    for i, entry in enumerate(data["history"], 1):
        question = entry.get("question", "")
        answer = entry.get("answer", "")
        timestamp = entry.get("timestamp", "")
        lines.append(f"## Q{i}: {question}")
        if timestamp:
            lines.append(f"*Asked at: {timestamp}*")
        lines.append("")
        lines.append(f"**A{i}:**\n")
        lines.append(answer.strip() if answer else "_No answer returned._")
        lines.append("\n---\n")

    md_content = "\n".join(lines)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{chat_id}.md")
    with open(file_path, "w") as f:
        f.write(md_content)
    print(f"Markdown file created: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_chat_markdown.py <chat_id> [api_url] [output_dir]")
        sys.exit(1)
    chat_id = sys.argv[1]
    api_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "chat_markdowns"
    fetch_and_save_chat_markdown(chat_id, api_url, output_dir)