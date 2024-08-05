webtoon_id = '812354'
webtoon_name='육아일기'
total_episodes=73


import element_manager as em
import mouse_controller as mouse
import time
import database_manager as db
def accessEpisodePage(episode_number:str):
    url = f'https://m.comic.naver.com/webtoon/detail?titleId={webtoon_id}&no={episode_number}'
    em.moveToPage(url)

def getTotalPanels():
    mouse.move_to_point(1083,978)
    mouse.click_left_button()
    element = em.findElement('.viewer_btns>.slider_num')
    total_panels=int(element.text.split('/')[1])
    return total_panels

def getImageURL():
    element = em.findElements('.swiper-lazy')[0]
    image_url = str(em.getValueFromAttribute(element, 'src'))
    return image_url

def getEpisodeID(image_url:str):
    image_filename=image_url.split('/')[6]
    episode_id = image_filename.split('_')[0]
    return episode_id

def make_panel_number(number:int):
    '''if number is '1', this function make it '001' '''
    result=''
    if number<10: result='00'+str(number)
    elif number<100: result='0'+str(number)
    return result

connection = db.getDBConnection()
cursor = db.getCursor(connection)
## 데이터베이스 초기화 코드
# db.initDatabase(connection,cursor)
# db.addWebtoonData(connection,cursor, [str(webtoon_id), str(webtoon_name), int(total_episodes)])


for episode_number in range(1,total_episodes+1):
    accessEpisodePage(str(episode_number))
    time.sleep(3)

    total_panels=getTotalPanels()
    first_image_url = getImageURL()
    episode_id = getEpisodeID(image_url=first_image_url)
    episode_url = f'https://m.comic.naver.com/webtoon/detail?titleId={webtoon_id}&no={episode_number}'
    db.addEpisodeData(connection,cursor, [str(episode_id), int(episode_number), str(episode_url), int(total_panels), str(webtoon_id)])
    for panel_number in range(1, total_panels):
        panel_number_str = make_panel_number(panel_number)
        image_url = f'https://image-comic.pstatic.net/mobilewebimg/{webtoon_id}/{episode_number}/{episode_id}_{panel_number_str}.jpg'
        db.addPanelData(connection, cursor, [str(episode_id), int(panel_number), str(image_url)])
        print(f'\t{panel_number}\t...수집완료')
    print(f'[{episode_number}]\t총 컷 개수:{total_panels}\t에피소드 아이디:{episode_id}\t...수집완료')
    