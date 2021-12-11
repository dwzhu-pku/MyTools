"""
    一个简单的爬虫脚本，可以直接利用链接把数据下载到服务器上。但是不能访问外网。
    如果还需要和目标网页进行交互（比如登录），那可能还需要改进一下这个脚本。
    其它情况下只要修改代码里面的以下部分即可：
        URL：目标地址
        Referer：你从哪个网址进入目标网页的（这个主要是为了反爬，通过浏览器可以查看，反爬措施弱的网页可以直接不管这一项）
        Cookie：访问目标网页时的Cookie（这个也是为了反爬，通过浏览器可以查看，反爬措施弱的网页可以直接不管这一项）
        FILENAME：写到本地的文件名
"""

import requests
import time

URL = "https://diskasu.pku.edu.cn:10002/Bucket/bab1d452-c23b-4d03-b766-329261bcc4d6/E9715606A14049D7B5BDAD170CD917BE/1E8EDA5CFF384EB3B25B9C54735E2672?response-content-disposition=attachment%3b%20filename%3d%22cl%255fcheckpoint%255f9.rar%22%3b%20filename*%3dutf%2d8%27%27cl%255fcheckpoint%255f9.rar&AWSAccessKeyId=ASE&Expires=1628155664&Signature=3W3kR9dPGZraQFKN0A71S0WsY2E%3d"
FILENAME = "checkpoint_9.rar"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47",
    "Referer": "https://disk.pku.edu.cn/",
    'Proxy-Connection':'keep-alive',
    # "Cookie": "Hm_lvt_28b2c13df26812abce37d6c193894f89=1597493753; UM_distinctid=174ae39a3fd120-0fe41695934467-7d647865-144000-174ae39a3fe1ce"

}

print("Started!")
html = requests.get(URL,headers=headers,stream = True,verify=False)
length = float(html.headers["content-length"])
print(html.status_code)
print("Length:{:.2f}M".format(length/(1024*1024)))

# 按二进制文件的形式写入
with open (FILENAME,'wb') as fout:
    lastTime = time.time()
    sizeCnt = 0
    sizeTmp = 0
    for chunk in html.iter_content(chunk_size=512):
        if chunk:
            fout.write(chunk)
            sizeCnt += len(chunk)
            # 每隔两秒打印一次进度
            if time.time() - lastTime> 2:
                p = sizeCnt/length * 100
                speed = (sizeCnt-sizeTmp) / (1024*1024*2)
                sizeTmp = sizeCnt
                print('Download: ' + '{:.2f}'.format(p) + '%' + ' Speed: ' + '{:.2f}'.format(speed) + 'M/S')
                lastTime = time.time()

        
print("Done")