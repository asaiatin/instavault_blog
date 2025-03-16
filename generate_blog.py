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
        "max_tokens": max_tokens,  # Limit response length
        "stream": False,  # Disable streaming for simplicity
    }
    try:
        print(f"Sending request to: {DEEPSEEK_API_URL}")  # Debugging
        print(f"Request payload: {json.dumps(data, indent=2)}")  # Debugging
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        print(f"Response status code: {response.status_code}")  # Debugging
        print(f"Response body: {response.text}")  # Debugging
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()["choices"][0]["message"]["content"].strip()  # Extract response
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

#RICH TEXT
def format_content_for_strapi(content):
    return [
        {
            "type": "paragraph",
            "children": [
                {
                    "type": "text",
                    "text": content,
                }
            ]
        }
    ]


# Function to publish to Strapi
def publish_to_strapi(title, content):
    headers = {
        "Authorization": f"Bearer {STRAPI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "data": {
            "Title": title,
            "Content": format_content_for_strapi(content),
        }
    }
    try:
        print(f"Sending request to: {STRAPI_API_URL}")  # Debugging
        print(f"Request payload: {json.dumps(data, indent=2)}")  # Debugging
        response = requests.post(STRAPI_API_URL, headers=headers, json=data)
        print(f"Response status code: {response.status_code}")  # Debugging
        print(f"Response body: {response.text}")  # Debugging
        response.raise_for_status()  # Raise an error for bad status codes
        print("Blog published to Strapi successfully!")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to publish to Strapi: {e}")

# Generate blog post
try:
    # Generate title
    title_prompt = "Generate a catchy title for a blog post about how to organize saved Instagram posts using InstaVault."
    title = generate_text(title_prompt, max_tokens=20)

    # Generate content
    content_prompt = "Write a 500-word blog post about how to organize saved Instagram posts using InstaVault. Focus on actionable tips and examples."
    content = generate_text(content_prompt, max_tokens=500)

    # Save title and content to a JSON file
    blog_data = {
        "title": title,
        "content": content,
    }
    with open("generated_blog.json", "w") as f:
        json.dump(blog_data, f)

    # Print JSON content to logs
    print("Generated JSON Content:")
    print(json.dumps(blog_data, indent=4))

    print("Blog title and content generated successfully!")

    # Publish to Strapi
    publish_to_strapi(title, content)

except Exception as e:
    print(f"Error: {e}")
