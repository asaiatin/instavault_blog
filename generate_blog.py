import os
import requests
import json
import datetime

# DeepSeek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Strapi API endpoint and key
STRAPI_API_URL = "https://strapi.instavault.co/api/blogs"
STRAPI_API_KEY = os.getenv("STRAPI_API_KEY")

# Function to call DeepSeek API
def generate_text(prompt, max_tokens):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are an award-winning SEO writer like Neil Patel. Your writing is data-driven, engaging, and optimized for search engines. You provide fresh, innovative, and actionable insights that resonate with readers and rank well on Google.",
            },
            {"role": "user", "content": prompt},  # User prompt
        ],
        "max_tokens": max_tokens,
        "stream": False,
    }

    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        print(f"Error generating text: {response.text}")
        return None

# Function to post to Strapi
def post_to_strapi(title, content):
    headers = {
        "Authorization": f"Bearer {STRAPI_API_KEY}",
        "Content-Type": "application/json",
    }

    formatted_content = [
        {"type": "heading", "level": 1, "children": [{"type": "text", "text": title}]},
        {"type": "paragraph", "children": [{"type": "text", "text": content}]},
    ]
    
    data = {
        "data": {
            "Title": title,
            "Content": formatted_content,
            "PublishedAt": datetime.datetime.utcnow().isoformat()
        }
    }
    
    response = requests.post(STRAPI_API_URL, headers=headers, json=data)
    if response.status_code == 201:
        print("Blog published successfully!")
    else:
        print(f"Error posting to Strapi: {response.text}")

if __name__ == "__main__":
    # Generate title
    title_prompt = "Generate a catchy title for a blog post about how to organize saved Instagram posts using InstaVault."
    title = generate_text(title_prompt, 20)
    
    if title:
        title = title.strip('"')  # Fix quote issue
        
        # Generate content
        content_prompt = "Write a detailed, well-formatted blog post about how to organize saved Instagram posts using InstaVault. Include step-by-step instructions, actionable tips, and proper HTML/Markdown formatting."
        content = generate_text(content_prompt, 500)
        
        if content:
            post_to_strapi(title, content)
