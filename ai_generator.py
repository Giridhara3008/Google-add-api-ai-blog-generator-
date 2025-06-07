from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_blog_post(keyword, seo_data):
    prompt = f"""
    Write an SEO-optimized blog post about '{keyword}'.
    Include sections, formatting, and 2 affiliate links like {{AFF_LINK_1}}, {{AFF_LINK_2}}.
    Post should have a title but don't put "Title" word in the output content.
    
    SEO Data:
    - Search Volume: {seo_data['search_volume']}
    - Difficulty: {seo_data['keyword_difficulty']}
    - CPC: {seo_data['avg_cpc']}
    Use above SEO data to optimize this blog post, dont use it in content
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful content writer."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    # Replace dummy affiliate placeholders
    content = content.replace("{{AFF_LINK_1}}", "https://dummy-affiliate1.com")
    content = content.replace("{{AFF_LINK_2}}", "https://dummy-affiliate2.com")

    return content
