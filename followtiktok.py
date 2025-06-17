import requests
import time
import random
import json
import webbrowser  # Thêm dòng này

username = input('Nhập Username Tik Tok (Không Nhập @ ): ')
success_count = 0

print(f"Bắt đầu tăng follow cho @{username}...")

# Mở trình duyệt để theo dõi trạng thái web
webbrowser.open('https://tikfollowers.com/free-tiktok-followers')

def get_random_user_agent():
    chrome_versions = [115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
    return f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)}.0.0.0 Safari/537.36'


while True:
    # Tạo headers mới mỗi lần để tránh bị chặn
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': get_random_user_agent(),
    }
    
    try:
        # Tạo session mới để lấy cookies
        session = requests.Session()
        access = session.get('https://tikfollowers.com/free-tiktok-followers', headers=headers, timeout=30)
        
        if 'ci_session' not in session.cookies:
            print('Không lấy được session, đang thử lại...')
            time.sleep(2)
            continue
            
        # Lấy token CSRF
        try:
            token = access.text.split("csrf_token = '")[1].split("'")[0]
        except:
            print('Không lấy được token, đang thử lại...')
            time.sleep(2)
            continue
            
        # Tìm kiếm người dùng
        search_data = json.dumps({
            "type": "follow",
            "q": f"@{username}",
            "google_token": "t",
            "token": token
        })
        
        search_response = session.post(
            'https://tikfollowers.com/api/free', 
            headers={**headers, 'content-type': 'application/json'}, 
            data=search_data
        )
        
        search = search_response.json()
        
        if search.get('success') == True:
            data_follow = search['data']
            
            # Gửi yêu cầu follow
            follow_data = json.dumps({
                "google_token": "t",
                "token": token,
                "data": data_follow,
                "type": "follow"
            })
            
            send_follow = session.post(
                'https://tikfollowers.com/api/free/send', 
                headers={**headers, 'content-type': 'application/json'}, 
                data=follow_data
            ).json()
            
            if send_follow.get('o') == 'Success!' and send_follow.get('success') == True:
                success_count += 1
                print(f'[+] Tăng Follow Tik Tok Thành Công - Tổng: {success_count}')
                # Đợi ngẫu nhiên một chút để tránh bị phát hiện
                time.sleep(random.uniform(1, 3))
                continue
                
            elif send_follow.get('o') == 'Oops...' and send_follow.get('success') == False:
                try:
                    message = send_follow.get('message', '')
                    print(f"[-] Lỗi: {message}")
                    
                    # Nếu phải chờ
                    if 'wait' in message.lower() or 'minutes' in message.lower():
                        # Chỉ chờ tối đa 30 giây bất kể trang yêu cầu chờ bao lâu
                        wait_time = random.randint(20, 30)
                        print(f"Đang đợi {wait_time} giây thay vì chờ đủ thời gian...")
                        
                        for i in range(wait_time, 0, -1):
                            print(f'Vui lòng chờ {i} giây...', end='\r')
                            time.sleep(1)
                    else:
                        # Lỗi khác, chỉ chờ 5 giây
                        time.sleep(5)
                except Exception as e:
                    print(f'Lỗi xử lý thông báo: {str(e)}')
                    time.sleep(5)
        else:
            print(f"[-] Không tìm thấy người dùng hoặc lỗi API: {search.get('message', 'Không có thông báo')}")
            time.sleep(5)
                
    except Exception as e:
        print(f'Lỗi không xác định: {str(e)}')
        # Đợi 5 giây trước khi thử lại
        time.sleep(5)