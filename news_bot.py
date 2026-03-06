import os, requests, smtplib, google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    # 讀取 Secrets
    news_key = os.getenv("NEWS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pw = os.getenv("GMAIL_APP_PASSWORD")

    # 1. 抓取新聞
    url = f"https://newsapi.org/v2/everything?q=AI&language=zh&pageSize=3&apiKey={news_key}"
    r = requests.get(url).json()
    articles = r.get('articles', [])
    news_content = "\n".join([f"標題: {a['title']}" for a in articles]) if articles else "今日無重大新聞"

    # 2. Gemini 生成 (換成絕對保險的最新穩定型號名稱)
    genai.configure(api_key=gemini_key)
    # 使用這個精確的型號名稱
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    
    try:
        response = model.generate_content(f"請摘要以下新聞：\n{news_content}")
        text = response.text
    except Exception as e:
        text = f"AI 生成失敗，錯誤原因: {str(e)}"

    # 3. 寄出信件
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 最終測試報告"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
