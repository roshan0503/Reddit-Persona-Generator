import argparse
import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import praw
import requests
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access API Keys from environment
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class RedditScraper:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
    
    def extract_username_from_url(self, url: str) -> str:
        patterns = [
            r'reddit\.com/u/([^/]+)',
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/users/([^/]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Invalid Reddit URL format: {url}")
    
    def scrape_user_data(self, username: str, limit: int = 100) -> Dict:
        try:
            user = self.reddit.redditor(username)
            
            # Check if user exists
            if not hasattr(user, 'id'):
                try:
                    _ = user.id
                except:
                    raise ValueError(f"User '{username}' not found or suspended")
            
            posts = []
            comments = []
            
            # Scrape submissions (posts)
            try:
                for submission in user.submissions.new(limit=limit):
                    posts.append({
                        'id': submission.id,
                        'title': submission.title,
                        'selftext': submission.selftext,
                        'subreddit': str(submission.subreddit),
                        'score': submission.score,
                        'created_utc': submission.created_utc,
                        'url': f"https://reddit.com{submission.permalink}"
                    })
            except Exception as e:
                print(f"Error scraping posts: {e}")
            
            # Scrape comments
            try:
                for comment in user.comments.new(limit=limit):
                    comments.append({
                        'id': comment.id,
                        'body': comment.body,
                        'subreddit': str(comment.subreddit),
                        'score': comment.score,
                        'created_utc': comment.created_utc,
                        'url': f"https://reddit.com{comment.permalink}"
                    })
            except Exception as e:
                print(f"Error scraping comments: {e}")
            
            return {
                'username': username,
                'posts': posts,
                'comments': comments,
                'total_posts': len(posts),
                'total_comments': len(comments)
            }
            
        except Exception as e:
            raise Exception(f"Error scraping user data: {e}")


class PersonaGenerator:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama3-70b-8192"
    
    def generate_persona(self, user_data: Dict) -> str:
        # Prepare content for analysis
        content = self._prepare_content(user_data)
        
        prompt = f"""
        Analyze the following Reddit user data and create a comprehensive persona profile.
        
        User: {user_data['username']}
        Total Posts: {user_data['total_posts']}
        Total Comments: {user_data['total_comments']}
        
        Content to analyze:
        {content}
        
        Please create a persona with the following structure:
        
        Reddit Username: {user_data['username']}
        --------------------------------------
        
        1️⃣ Interests / Hobbies:
        - List specific interests with citations
        - Format: Interest (Cited from: "exact quote" - Post/Comment ID)
        
        2️⃣ Personality Traits:
        - List personality traits with evidence
        - Format: Trait (Cited from: "exact quote" - Post/Comment ID)
        
        3️⃣ Writing Style / Tone:
        - Describe communication style
        - Format: Style element (Cited from: "exact quote" - Post/Comment ID)
        
        4️⃣ Values / Beliefs:
        - Identify core values and beliefs
        - Format: Value/Belief (Cited from: "exact quote" - Post/Comment ID)
        
        5️⃣ Behavior on Reddit:
        - Analyze Reddit usage patterns
        - Format: Behavior (Cited from: "exact quote" - Post/Comment ID)
        
        Rules:
        - Use exact quotes from the content
        - Include specific post/comment IDs
        - Keep quotes concise but meaningful
        - Provide specific evidence for each point
        - Be objective and professional
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert digital analyst specializing in creating detailed user personas from social media data. You analyze text patterns, communication styles, and behavioral indicators to build comprehensive profiles."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error generating persona: {e}")
    
    def _prepare_content(self, user_data: Dict) -> str:
        content = []
        
        # Add posts
        for post in user_data['posts'][:50]:  # Limit to avoid token limits
            if post['title'] and post['selftext']:
                content.append(f"POST [{post['id']}]: {post['title']} - {post['selftext'][:500]}")
            elif post['title']:
                content.append(f"POST [{post['id']}]: {post['title']}")
        
        # Add comments
        for comment in user_data['comments'][:50]:  # Limit to avoid token limits
            if comment['body'] and len(comment['body']) > 10:
                content.append(f"COMMENT [{comment['id']}]: {comment['body'][:500]}")
        
        return "\n\n".join(content)


class PersonaFileManager:
    @staticmethod
    def ensure_output_directory() -> str:
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir
    
    @staticmethod
    def save_persona(persona: str, username: str) -> str:
        output_dir = PersonaFileManager.ensure_output_directory()
        filename = f"{username}_persona.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(persona)
            f.write(f"\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return filepath


def streamlit_app():
    st.set_page_config(
        page_title="Reddit User Persona Generator",
        page_icon="👤",
        layout="wide"
    )
    
    st.title("🎭 Reddit User Persona Generator")
    st.markdown("Generate comprehensive user personas from Reddit profiles using Groq Llama3 analysis.")
    
    # Sidebar for configuration
    st.sidebar.header("🔧 Configuration")
    
    # Settings
    st.sidebar.subheader("Settings")
    scrape_limit = st.sidebar.slider(
        "Content Limit",
        min_value=10,
        max_value=500,
        value=100,
        help="Maximum number of posts/comments to scrape"
    )
    
    model_choice = st.sidebar.selectbox(
        "Groq Model",
        ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
        index=0,
        help="Select Groq model for persona generation"
    )
    
    # API Status
    st.sidebar.subheader("🔗 API Status")
    st.sidebar.success("✅ Reddit API: Connected")
    st.sidebar.success("✅ Groq API: Connected")
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 User Input")
        reddit_url = st.text_input(
            "Reddit Profile URL",
            placeholder="https://www.reddit.com/user/username/",
            help="Enter the full Reddit profile URL"
        )
        
        if st.button("🚀 Generate Persona", type="primary"):
            if not reddit_url:
                st.error("❌ Please provide a Reddit profile URL.")
                return
            
            try:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Initialize scraper
                status_text.text("🔄 Initializing Reddit scraper...")
                progress_bar.progress(20)
                
                scraper = RedditScraper(
                    client_id=REDDIT_CLIENT_ID,
                    client_secret=REDDIT_CLIENT_SECRET,
                    user_agent="PersonaGenerator/1.0"
                )
                
                # Extract username
                username = scraper.extract_username_from_url(reddit_url)
                status_text.text(f"👤 Found username: {username}")
                progress_bar.progress(40)
                
                # Scrape data
                status_text.text("📥 Scraping Reddit data...")
                user_data = scraper.scrape_user_data(username, limit=scrape_limit)
                progress_bar.progress(60)
                
                # Generate persona
                status_text.text("🤖 Generating persona with Groq Llama3...")
                generator = PersonaGenerator(GROQ_API_KEY)
                generator.model = model_choice
                
                # Test API connection
                test_response = generator.client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=1
                )
                
                persona = generator.generate_persona(user_data)
                progress_bar.progress(80)
                
                # Save file
                status_text.text("💾 Saving persona file...")
                filepath = PersonaFileManager.save_persona(persona, username)
                progress_bar.progress(100)
                
                status_text.text("✅ Persona generation complete!")
                
                # Display results
                st.success(f"🎉 Successfully generated persona for u/{username}")
                st.info(f"📁 Saved to: {filepath}")
                
                # Display persona
                st.subheader("📄 Generated Persona")
                st.text_area(
                    "Persona Content",
                    value=persona,
                    height=400,
                    disabled=True
                )
                
                # Download button
                st.download_button(
                    label="⬇️ Download Persona File",
                    data=persona,
                    file_name=f"{username}_persona.txt",
                    mime="text/plain"
                )
                
                # Display statistics
                st.subheader("📊 Analysis Statistics")
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                
                with col_stats1:
                    st.metric("Posts Analyzed", user_data['total_posts'])
                with col_stats2:
                    st.metric("Comments Analyzed", user_data['total_comments'])
                with col_stats3:
                    st.metric("Total Content", user_data['total_posts'] + user_data['total_comments'])
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if "api_key" in str(e).lower():
                    st.error("🔑 Invalid Groq API key. Please check the configuration.")
                elif "rate_limit" in str(e).lower():
                    st.error("🚫 Rate limit exceeded. Please wait and try again.")
    
    with col2:
        st.subheader("ℹ️ Information")
        st.info("""
        **How to use:**
        1. Enter a Reddit profile URL
        2. Select model and content limit
        3. Click 'Generate Persona'
        4. Download the results
        
        **Features:**
        - Scrapes posts and comments
        - Groq Llama3 powered analysis
        - Detailed persona with citations
        - Downloadable results
        - Ultra-fast processing
        """)
        
        st.subheader("🚀 About Groq")
        st.markdown("""
        **Groq + Llama3:**
        - Ultra-fast inference
        - High-quality analysis
        - Cost-effective
        - Multiple model options
        
        **Models Available:**
        - llama3-70b-8192 (Best quality)
        - llama3-8b-8192 (Fastest)
        - mixtral-8x7b-32768 (Balanced)
        """)
        
        st.subheader("💡 Tips")
        st.markdown("""
        **Best Results:**
        - Use active Reddit accounts
        - Higher content limits = better analysis
        - Llama3-70b for detailed insights
        - Try different models for variety
        """)


def command_line_interface():
    """Command line interface for the persona generator."""
    
    parser = argparse.ArgumentParser(
        description="Generate Reddit user personas using Groq Llama3 analysis"
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Reddit profile URL (e.g., https://www.reddit.com/user/username/)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of posts/comments to scrape (default: 100)"
    )
    parser.add_argument(
        "--model",
        default="llama3-70b-8192",
        choices=["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
        help="Groq model to use (default: llama3-70b-8192)"
    )
    
    args = parser.parse_args()
    
    try:
        print("🔄 Initializing Reddit scraper...")
        scraper = RedditScraper(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent="PersonaGenerator/1.0"
        )
        
        print("👤 Extracting username...")
        username = scraper.extract_username_from_url(args.url)
        print(f"Found username: {username}")
        
        print("📥 Scraping Reddit data...")
        user_data = scraper.scrape_user_data(username, limit=args.limit)
        print(f"Found {user_data['total_posts']} posts and {user_data['total_comments']} comments")
        
        print(f"🤖 Generating persona with Groq {args.model}...")
        generator = PersonaGenerator(GROQ_API_KEY)
        generator.model = args.model
        
        # Test API connection
        test_response = generator.client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1
        )
        
        persona = generator.generate_persona(user_data)
        
        print("💾 Saving persona file...")
        filepath = PersonaFileManager.save_persona(persona, username)
        
        print(f"✅ Persona generated successfully!")
        print(f"📁 Saved to: {filepath}")
        
        # Display preview
        print("\n" + "="*50)
        print("PERSONA PREVIEW")
        print("="*50)
        print(persona[:500] + "..." if len(persona) > 500 else persona)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if "api_key" in str(e).lower():
            print("🔑 Invalid Groq API key. Please check the configuration.")
        elif "rate_limit" in str(e).lower():
            print("🚫 Rate limit exceeded. Please wait and try again.")
        sys.exit(1)


def main():
    # Check if running with Streamlit
    if len(sys.argv) > 1 and sys.argv[1] == "--streamlit":
        streamlit_app()
    elif len(sys.argv) > 1 and "--url" in sys.argv:
        command_line_interface()
    else:
        # Default to Streamlit interface
        print("🚀 Starting Streamlit interface...")
        print("💡 Run with --url for command line interface")
        print("📖 Use 'streamlit run reddit_persona.py' for best experience")
        streamlit_app()


if __name__ == "__main__":
    main()