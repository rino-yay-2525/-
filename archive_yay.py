import asyncio
import noble_tls
from noble_tls import Client
import time

user_id = ""
proxy = ""

session = noble_tls.Session(client=Client.CHROME_120,random_tls_extension_order=True)

async def archive(url):
    headers = {
        'authority': 'archive.is',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ja',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    r_1 = await session.get('https://archive.is/', headers=headers,proxy=proxy)
    submit_id = str(r_1.content).split('name="submitid', 1)[1].split('value="', 1)[1].split('"', 1)[0]

    params = {
        'submitid': submit_id,
        'url': url,
    }
    r_2 = await session.get('https://archive.is/submit/', params=params, headers=headers,proxy=proxy)
    if r_1.status_code == 200 and r_2.status_code == 200:
        result = 'https://archive.is/' + str(r_2.text).split('https://archive.is/wip/', 1)[1].split('"', 1)[0]
        with open("file.txt","a") as f:
            f.write(f"{result}\n")
        print(f"success → {result}")
    else:
        print("failure")

async def main():
    list = []

    headers = {
        'Host': 'api.yay.space',
        'User-Agent': 'yay 3.32.0 android 13 (2.0x 2560x1800 sdk_gphone_x86_64)',
        'X-App-Version': '3.32',
        'X-Device-Info': 'yay 3.32.0 android 13 (2.0x 2560x1800 sdk_gphone_x86_64)',
        'X-Device-Uuid': 'ada84d656f8f0605',
        'X-Device-Id': '5941f3212fae836e7e707ccae3ac04d6833a9ad5',
        'X-Client-Ip': '106.146.194.45',
        'X-Connection-Type': 'wifi',
        'X-Connection-Speed': '0 kbps',
        'Accept-Language': 'ja',
        # 'Accept-Encoding': 'gzip, deflate, br',
    }

    print("\n＜全投稿取得 開始＞\n")
    response = await session.get(f"https://api.yay.space/v2/posts/user_timeline?number=100&user_id={user_id}",headers=headers)
    list_sub = []
    for i in range(100):
        try:
            id = str(response.json()['posts'][i]['id'])
            list_sub.append(id)
        except:
            continue
    list += list_sub

    while True:
        if list_sub == []:
            break
        print(list_sub[-1])
        response = await session.get(f"https://api.yay.space/v2/posts/user_timeline?from_post_id={list_sub[-1]}&number=100&user_id={user_id}",headers=headers)
        list_sub = []
        for i in range(100):
            try:
                id = str(response.json()['posts'][i]['id'])
                list_sub.append(id)
            except:
                continue
        list += list_sub

    print("\n")
    print(list)
    print("\n＜全投稿取得 完了＞")
    print(f"合計：{len(list)}個\n")
    time.sleep(5)

    print(f"＜魚拓登録 開始＞\n")
    for s in list:
        await archive("https://yay.space/post/" + s)
    print(f"\n＜魚拓登録 完了＞\n")

if __name__ == "__main__":
    asyncio.run(main())
