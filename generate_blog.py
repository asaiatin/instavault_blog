import os
import requests
import json
import datetime

# DeepSeek API endpoint and key
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# List of 30 InstaVault-aligned blog topics
topics = [
    "How to Organize Your Saved Instagram Posts Like a Pro",
    "Why Instagram’s Native ‘Saved’ Feature Isn’t Enough",
    "From Chaos to Order: How to Turn Your Saved Instagram Posts into a Knowledge Hub",
    "How Marketers Can Use InstaVault to Save and Organize Instagram Inspiration",
    "Top Instagram Trends for 2024 and How to Save Them for Later",
    "How to Build a Content Calendar Using Your Saved Instagram Posts",
    "How to Save and Organize Instagram Recipes with InstaVault",
    "Travel Planning Made Easy: How to Save and Organize Instagram Travel Guides",
    "DIY Inspiration: How to Organize Saved Instagram Tutorials with InstaVault",
    "How to Turn Your Saved Instagram Posts into a Personal Knowledge Base",
    "The Ultimate Guide to Organizing Your Digital Life with InstaVault",
    "How to Rediscover Forgotten Instagram Posts with InstaVault",
    "How InstaVault’s Automated Categorization Saves You Time",
    "Using InstaVault’s Dashboard to Stay on Top of Your Saved Posts",
    "How to Use InstaVault’s Weekly Newsletter to Stay Inspired",
    "10 Instagram Features You’re Not Using (But Should Be)",
    "How to Save Instagram Posts for Later Without Losing Them",
    "The Best Instagram Accounts to Follow for [Your Niche]",
    "How to Use Instagram Saved Posts for SEO Inspiration",
    "Content Repurposing: How to Turn Saved Instagram Posts into Blog Content",
    "How to Use InstaVault to Track Competitor Content for SEO",
    "How to Use Instagram to Build a Personal Learning Library",
    "How to Save and Organize Instagram Posts for Personal Development",
    "How to Create a Vision Board Using Saved Instagram Posts",
    "How Real Estate Agents Can Use InstaVault to Save and Organize Listings",
    "How Food Bloggers Can Use InstaVault to Save and Organize Recipes",
    "How Travel Influencers Can Use InstaVault to Save and Organize Destinations",
    "The Future of Instagram Bookmarking: Trends to Watch in 2024",
    "How AI is Transforming Instagram Bookmarking with Tools Like InstaVault",
    "Why InstaVault is the Ultimate Tool for Instagram Power Users",
]

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
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        print(f"Response status code: {response.status_code}")  # Debugging
        print(f"Response body: {response.text}")  # Debugging
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()["choices"][0]["message"]["content"].strip()  # Extract response
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

# Get today's date and calculate the index for topics
today = datetime.datetime.now()
topic_index = (today.day - 1) % len(topics)  # Rotate topics daily

# Select topic
topic = topics[topic_index]

# Generate title
try:
    title_prompt = f"Write a blog post about: {topic}"
    title = topic  # Use the topic as the title
except Exception as e:
    print(f"Failed to generate title: {e}")
    raise

# Generate content
try:
    content_prompt = f"Write a 500-word blog post about: {topic}. Focus on how InstaVault can help users solve this problem. Include actionable tips and examples."
    content = generate_text(content_prompt, max_tokens=500)
except Exception as e:
    print(f"Failed to generate content: {e}")
    raise

# Save title and content to a JSON file
blog_data = {
    "title": title,
    "content": content,
}
with open("generated_blog.json", "w") as f:
    json.dump(blog_data, f)

print("Blog title and content generated successfully!")
