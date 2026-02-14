import requests
from datetime import datetime
import json
import base64
import random
import os

username = os.getenv("GITHUB_REPOSITORY_OWNER")
if not username:
    print("⚠️ 깃허브 아이디를 찾을 수 없습니다. 환경 변수를 확인하세요.")
    exit()

url = f"https://api.github.com/users/{username}/events"

try:
    response = requests.get(url)
    events = response.json()
    today = datetime.now().strftime("%Y-%m-%d")

    today_commits = 0
    for event in events:
        if event["type"] == "PushEvent" and event["created_at"].startswith(today):
            today_commits += 1

    with open("fortunes.json", "r", encoding="utf-8") as f:
        fortunes_db = json.load(f)

    if today_commits <= 1:
        category = "low"
    elif 2 <= today_commits <= 5:
        category = "medium"
    else:
        category = "high"

    all_possible = fortunes_db[category] + fortunes_db["random"]
    my_fortune = random.choice(all_possible)

    try:
        with open("Lucky.png", "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode("utf-8")
            img_data = f"data:image/png;base64,{encoded_img}"
    except FileNotFoundError:
        img_data = ""

    svg_content = f"""
    <svg width="450" height="280" viewBox="0 0 450 280" fill="none" xmlns="http://www.w3.org/2000/svg">
        <foreignObject width="100%" height="100%">
            <div xmlns="http://www.w3.org/1999/xhtml">
                <style>
                    .fortune-card {{
                        width: 450px; 
                        height: 280px; 
                        background: #1a1a1a;
                        border-radius: 20px; 
                        padding: 28px; 
                        color: #f5f5f5;
                        font-family: 'Segoe UI', Roboto, sans-serif; 
                        box-sizing: border-box;
                        display: flex;
                        flex-direction: column;
                    }}
                    .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
                    .title {{ font-size: 15px; color: #f0f6fc; font-weight: 600; letter-spacing: 0.5px; }}
                    .clover {{ width: 65px; height: 65px; animation: float 3s ease-in-out infinite; }}
                    @keyframes float {{ 0%, 100% {{ transform: translateY(0) rotate(0); }} 50% {{ transform: translateY(-8px) rotate(5deg); }} }}
                    .stats-section {{ display: flex; align-items: center; gap: 12px; margin-bottom: 15px; }}
                    .grass-icon {{ width: 14px; height: 14px; background-color: #39d353; border-radius: 3px; }}
                    .commit-count {{ font-size: 26px; font-weight: bold; color: #f0f6fc; }}
                    .commit-label {{ font-size: 14px; color: #8b949e; margin-left: 5px; }}
                    .divider {{ height: 1px; background-color: #30363d; margin: 15px 0; }}
                    .fortune-text {{ font-size: 16px; line-height: 1.7; color: #f5f5f5; flex-grow: 1; }}
                    .footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 15px; font-size: 12px; color: #484f58; }}
                </style>
                <div class="fortune-card">
                    <div class="card-header">
                        <div class="title">오늘의 코딩운세</div>
                        <img src="{img_data}" class="clover" />
                    </div>
                    <div class="stats-section">
                        <div class="grass-icon"></div>
                        <div>
                            <span class="commit-count">{today_commits}</span>
                            <span class="commit-label">Commits Today</span>
                        </div>
                    </div>
                    <div class="divider"></div>
                    <div class="fortune-text">{my_fortune}</div>
                    <div class="footer">
                        <span>GitHub @{username}</span>
                        <span>{today}</span>
                    </div>
                </div>
            </div>
        </foreignObject>
    </svg>
    """

    with open("fortune.svg", "w", encoding="utf-8") as f:
        f.write(svg_content)

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(
            {{"date": today, "commits": today_commits, "fortune": my_fortune}},
            f,
            ensure_ascii=False,
            indent=4,
        )

    print(f"✅ 성공! 오늘의 아이디: {{username}} / 운세: {{my_fortune}}")

except Exception as e:
    print(f"⚠️ 에러 발생: {{e}}")
