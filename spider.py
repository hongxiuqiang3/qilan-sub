import re
import base64
from playwright.sync_api import sync_playwright

url = "https://www.qilan.de/nodes"

try:
    # 启动云端真实浏览器引擎
    with sync_playwright() as p:
        print("🚀 启动云端无头浏览器 (真实 Chrome 内核)...")
        browser = p.chromium.launch(headless=True)
        
        # 披上极品伪装服
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("🌐 正在潜入目标网页，耐心等待 JS 动态加载...")
        # wait_until="networkidle" 是魔法指令：等网页不再有网络请求了（说明动态内容加载完了）再动手
        page.goto(url, wait_until="networkidle", timeout=30000)
        
        # 强行再蛰伏 3 秒，确保对方的节点已经完全显示在页面上
        page.wait_for_timeout(3000)
        
        html = page.content()
        browser.close()

    print("🩻 网页真实 DOM 提取完毕，开始雷达扫描...")
    
    # 精准捕捉各种协议节点
    pattern = r'(?:vmess|vless|ss|ssr|trojan)://[a-zA-Z0-9+/=]+'
    nodes = list(set(re.findall(pattern, html)))

    if nodes:
        print(f"✅ 太帅了！成功抓取到 {len(nodes)} 个动态节点！")
        raw_text = '\n'.join(nodes)
        b64_text = base64.b64encode(raw_text.encode('utf-8')).decode('utf-8')
        
        with open('sub.txt', 'w') as f:
            f.write(b64_text)
        print("🎉 专属订阅文件 sub.txt 锻造成功！")
    else:
        print("❌ 依然没找到节点。对方可能启用了最高级的真人验证 (如 Cloudflare 5秒盾)。")
        open('sub.txt', 'w').close()

except Exception as e:
    print(f"💥 潜入失败，报错信息: {e}")
    open('sub.txt', 'w').close()
