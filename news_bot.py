import os
import requests
import smtplib
import google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    # 讀取 Secrets
    news_key = os.getenv("NEWS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pw = os.getenv("GMAIL_APP_PASSWORD")

    # 1. 抓取新聞
    url = f"https://newsapi.org/v2/everything?q=AI&language=zh&sortBy=publishedAt&pageSize=3&apiKey={news_key}"
    articles = requests.get(url).json().get('articles', [])
    news_content = "\n".join([f"標題: {a['title']}" for a in articles])

    # 2. Gemini 生成
    genai.configure(api_key=gemini_key)
    # 換成最老牌、絕對存在的型號名稱
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"請摘要以下 AI 新聞並給出商業建議：\n\n{news_content}"
    response = model.generate_content(prompt)

    # 3. 寄出信件
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 AI 商業情報 (最終暴力修正版)"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(response.text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
