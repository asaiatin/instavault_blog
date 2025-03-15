import os
import requests

# Access the API key from the environment variable
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY environment variable is not set!")

# Example API call using the key
url = "https://api.deepseek.com/v1/generate"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}
data = {
    "prompt": "Write a 500-word blog post about the benefits of AI in SEO.",
    "max_tokens": 500,
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    blog_content = response.json()["choices"][0]["text"]
    with open("generated_blog.json", "w") as f:
        f.write(json.dumps({"content": blog_content}))
    print("Blog generated successfully!")
else:
    print(f"Failed to generate blog: {response.text}")
