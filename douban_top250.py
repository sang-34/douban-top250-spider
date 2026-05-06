import csv
import httpx
import re

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Microsoft Edge";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36 Edg/147.0.0.0',
    # 'cookie': 'bid=oH1LD2CEiQc; _pk_id.100001.4cf6=cd679dd67e1bdafe.1775459304.; __yadk_uid=H05VqWjJVMThkJCdo4LGvjTxyAjmsOwL; ll="118124"; __utmz=30149280.1775651464.2.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1775651482.2.2.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1777993989%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.4cf6=1; ap_v=0,6.0; __utma=30149280.1649051239.1775459305.1775739884.1777993990.5; __utmb=30149280.0.10.1777993990; __utmc=30149280; __utma=223695111.2010735708.1775459305.1775739884.1777993990.5; __utmb=223695111.0.10.1777993990; __utmc=223695111',
}

data = [
    ["电影名称", "导演", "上映时间", "评分"]
]

with httpx.Client() as client:
    try:
        response = client.get('https://movie.douban.com/top250', headers=headers)
        # print(response.text)

        if response.status_code == 200:
            content = response.text

            pattern1 = '<li>.*?<a.*?<span class="title">(.*?)</span>'
            pattern2 = '<li>.*?<a.*?<span class="title">(.*?)</span>.*?<div class="bd">.*?导演: (.*?)&'
            pattern3 = '<li>.*?<a.*?<span class="title">(.*?)</span>.*?<div class="bd">.*?导演: (.*?)&.*?v:average">(.*?)</span>'
            pattern4 = r'<li>.*?title">(.*?)</span>.*?导演: (.*?)&.*?<br>\s+(.*?)&.*?v:average">(.*?)</span>'

            results = re.findall(pattern4, content, re.S)

            for result in results:
                if result:
                    data.append(list(result))

            with open("豆瓣电影.csv", "w", encoding="utf-8-sig", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)

    except httpx.HTTPError as e:
        print(e)




