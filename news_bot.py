import os, requests, smtplib, google.generativeai as genai
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def run():
    # 1. 取得環境變數
    news_key = os.getenv("NEWS_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    gmail_user = os.getenv("GMAIL_USER")
    gmail_pw = os.getenv("GMAIL_APP_PASSWORD")
    
    # 2. 抓取新聞
    url = f"https://newsapi.org/v2/everything?q=AI&language=zh&pageSize=3&apiKey={news_key}"
    try:
        r = requests.get(url).json()
        articles = r.get('articles', [])
        content = "\n".join([f"標題: {a['title']}" for a in articles]) if articles else "今日無新聞"
    except:
        content = "新聞抓取失敗"

    # 3. Gemini 生成 (這次使用絕對正確的型號：gemini-1.5-flash)
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        # 加上更明確的指令
        response = model.generate_content(f"請用中文簡短摘要以下新聞：\n{content}")
        text = response.text
    except Exception as e:
        text = f"AI 生成失敗，原因：{str(e)}"

    # 4. 寄出郵件
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 恭喜！AI 情報正式成功"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
