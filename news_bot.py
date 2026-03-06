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

    # 2. 自動偵測型號
    genai.configure(api_key=gemini_key)
    try:
        # 抓取該 Key 真正擁有的型號列表
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # 優先用 flash，沒有的話用清單第一個
        target = next((m for m in models if 'flash' in m), models[0] if models else 'gemini-1.5-flash')
        
        model = genai.GenerativeModel(target)
        response = model.generate_content(f"請用中文簡短摘要：\n{content}")
        text = response.text
    except Exception as e:
        text = f"偵測到的型號: {str(models if 'models' in locals() else 'None')}\n錯誤細節: {str(e)}"

    # 3. 寄信
    msg = MIMEMultipart()
    msg['Subject'] = "🤖 AI 日報 (終極自動偵測版)"
    msg['From'] = gmail_user
    msg['To'] = "yehichun0907@gmail.com"
    msg.attach(MIMEText(text, 'plain'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(gmail_user, gmail_pw)
        server.sendmail(gmail_user, "yehichun0907@gmail.com", msg.as_string())

if __name__ == "__main__":
    run()
