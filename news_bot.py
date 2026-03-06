import os, requests, smtplib, google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    news_key = os.getenv("NEWS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pw = os.getenv("GMAIL_APP_PASSWORD")

    # 1. 抓取新聞
    url = f"https://newsapi.org/v2/everything?q=AI&language=zh&pageSize=3&apiKey={news_key}"
    articles = requests.get(url).json().get('articles', [])
    news_content = "\n".join([f"標題: {a['title']}" for a in articles])

    # 2. Gemini 生成 (使用最穩定的 gemini-pro)
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"摘要：{news_content}")

    # 3. 寄出信件
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 AI 情報 (成功版)"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(response.text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
