import os, requests, smtplib, google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    news_key, gemini_key = os.getenv("NEWS_API_KEY"), os.getenv("GEMINI_API_KEY")
    gmail_user, gmail_pw = os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD")
    
    # 1. 抓新聞
    url = f"https://newsapi.org/v2/everything?q=AI&language=zh&pageSize=3&apiKey={news_key}"
    r = requests.get(url).json()
    articles = r.get('articles', [])
    content = "\n".join([f"標題: {a['title']}" for a in articles]) if articles else "今日無新聞"

    # 2. Gemini 生成 (使用目前最通用的型號)
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(f"摘要新聞：{content}")
        summary = response.text
    except:
        summary = "AI 生成摘要失敗"

    # 3. 寄信
    msg = MIMEMultipart()
    msg['Subject'], msg['From'], msg['To'] = "🤖 最終測試成功", gmail_user, "yehichun0907@gmail.com"
    msg.attach(MIMEText(summary, 'plain'))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
