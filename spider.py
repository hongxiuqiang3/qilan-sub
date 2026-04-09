import urllib.request
import re
import base64

# 你想白嫖的节点网站
url = "https://www.qilan.de/nodes"

try:
    # 伪装成正规浏览器访问
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')

    # 🕸️ 终极正则引擎：精准抽离所有 vmess/vless/trojan/ss 链接
    pattern = r'(?:vmess|vless|ss|ssr|trojan)://[^\s\'"<>]+'
    nodes = list(set(re.findall(pattern, html)))

    if nodes:
        print(f"✅ 成功抓取到 {len(nodes)} 个节点！")
        # 将节点拼接，并转换成软路由通用的 Base64 订阅格式
        raw_text = '\n'.join(nodes)
        b64_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
        
        # 写入订阅文件
        with open('sub.txt', 'w') as f:
            f.write(b64_text)
        print("🎉 专属订阅文件 sub.txt 锻造成功！")
    else:
        print("❌ 未找到任何节点，可能网页结构已改或被防爬虫盾拦截。")

except Exception as e:
    print(f"💥 抓取失败，报错信息: {e}")
