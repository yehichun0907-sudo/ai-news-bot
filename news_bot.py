import os, requests, smtplib, google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    news_key, gemini_key = os.getenv("NEWS_API_KEY"), os.getenv("GEMINI_API_KEY")
    gmail_user, gmail_pw = os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD")
    
    # 1. 抓新聞
    url = f"https://newsapi.org/v2/everything?q=AI&language=zh&pageSize=3&apiKey={news_key}"
    try:
        r = requests.get(url).json()
        articles = r.get('articles', [])
        content = "\n".join([f"標題: {a['title']}" for a in articles]) if articles else "今日無新聞"
    except:
        content = "新聞抓取失敗"

    # 2. Gemini 生成 (這是最純粹的型號名稱寫法)
    genai.configure(api_key=gemini_key)
    
    # 【關鍵修正】拿掉 models/，直接用型號名
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content(f"請用中文摘要：\n{content}")
        text = response.text
    except Exception as e:
        # 如果還是失敗，我們讓它把錯誤細節噴出來
        text = f"AI 生成失敗，細節: {str(e)}"

    # 3. 寄信
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 AI 情報 (這是最後一搏了)"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
