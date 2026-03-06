import os
import requests
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    # 從 GitHub Secrets 讀取鑰匙
    news_key = os.getenv("NEWS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pw = os.getenv("GMAIL_APP_PASSWORD")

    # 1. 抓取 AI 商業新聞 (搜尋 business opportunity)
    url = f"https://newsapi.org/v2/everything?q=AI+business+opportunity&language=en&sortBy=publishedAt&pageSize=3&apiKey={news_key}"
    articles = requests.get(url).json().get('articles', [])
    news_content = "\n".join([f"Title: {a['title']}\nDesc: {a['description']}" for a in articles])

    # 2. Gemini 生成摘要
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"你是一位 AI 商業顧問，請將以下新聞用繁體中文摘要，並為一人公司提供 3 個具體變現建議：\n\n{news_content}"
    response = model.generate_content(prompt)

    # 3. 寄出信件
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 今日 AI 商業情報 (Vibe Coding MVP)"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(response.text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
