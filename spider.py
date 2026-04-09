import urllib.request
import re
import base64
import ssl

url = "https://www.qilan.de/nodes"

# 🎭 终极伪装：模拟真实的 Windows Chrome 浏览器，骗过基础爬虫盾
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.google.com/'
}

# 忽略 SSL 证书报错
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    print("🚀 正在伪装成浏览器潜入目标网站...")
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req, timeout=15, context=ctx)
    html = response.read().decode('utf-8')

    # 🕸️ 兼容性更强的正则提取
    pattern = r'(?:vmess|vless|ss|ssr|trojan)://[a-zA-Z0-9+/=]+'
    nodes = list(set(re.findall(pattern, html)))

    if nodes:
        print(f"✅ 成功抓取到 {len(nodes)} 个节点！")
        raw_text = '\n'.join(nodes)
        b64_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
        
        with open('sub.txt', 'w') as f:
            f.write(b64_text)
        print("🎉 专属订阅文件 sub.txt 锻造成功！")
    else:
        print("❌ 突破了防御，但网页里没找到节点代码！(可能是动态加载的)")
        open('sub.txt', 'w').close() # 创个空文件，防止后面的 git 报错

except Exception as e:
    print(f"💥 潜入失败，被防火墙击落: {e}")
    open('sub.txt', 'w').close() # 同样创个空文件保底
