import os
import requests
import json

# DeepSeek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/generate"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Function to call DeepSeek API
def generate_text(prompt, max_tokens):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",  # Fixed syntax
    }
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        raise Exception(f"Failed to generate text: {response.text}")

# Generate title
title_prompt = "Generate a catchy title for a blog post about the benefits of AI in SEO."
title = generate_text(title_prompt, max_tokens=20)

# Generate content
content_prompt = "Write a 500-word blog post about the benefits of AI in SEO."
content = generate_text(content_prompt, max_tokens=500)

# Save title and content to a JSON file
blog_data = {
    "title": title,
    "content": content,
}
with open("generated_blog.json", "w") as f:
    json.dump(blog_data, f)

print("Blog title and content generated successfully!")
