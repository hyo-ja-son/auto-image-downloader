import database_manager as db
import requests
import os

connection = db.getDBConnection()
cursor = db.getCursor(connection)


def download_image(image_url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP 오류가 발생했는지 확인

        # 이미지 데이터를 파일로 저장
        with open(save_path, "wb") as file:
            file.write(response.content)

        print(f"{save_path}\t...저장완료")
    except requests.exceptions.RequestException as e:
        print(f"{save_path}\t...저장실패")
        print(e)


cursor.execute(
    """
    SELECT webtoon.name, episode.episode_number, panel.panel_number, panel.image_url 
    FROM episode, panel, webtoon
    WHERE webtoon.webtoon_id = episode.webtoon_id 
    AND episode.episode_id = panel.episode_id
"""
)

rows = cursor.fetchall()

for row in rows:
    webtoon_name, episode_number, panel_number, image_url = row
    save_path = os.path.join(
        f"../data/{webtoon_name}", f"{episode_number}_{panel_number}.jpg"
    )
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    download_image(image_url, save_path)

# 데이터베이스 연결 종료
db.closeDatabaseConnection(connection)
