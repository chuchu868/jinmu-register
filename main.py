#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金木集团订货系统 - 通用Web注册工具
手机电脑通用版本
修复编码问题，兼容所有环境
"""

# ============== 导入库 ==============
import sys
import os
import json
import time
import base64
import socket
import webbrowser
import subprocess
from urllib.parse import parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO

# 尝试导入网络请求和加密库
try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("警告: requests库未安装，将无法发送API请求")

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad

    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("警告: pycryptodome库未安装，加密功能不可用")

# ============== 配置 ==============
INVITE_CODES = {
    "秦(705395969)": "705395969",
    "二姨(708642531)": "708642531",
}

# 加密密钥
ENCRYPT_KEY = "hfb6540l38b489d9f306a5b8e105334b"
ENCRYPT_IV = "hfb5cd0045222c52"

# API地址
SMS_API = "https://api.jinmu12.com/api/v1/5b5bdc44796e8"
REGISTER_API = "https://api.jinmu12.com/api/v1/5cad9f63e4f94"

HEADERS = {
    "Content-Type": "application/json",
    "Platform": "h5",
    "Referer": "https://classone.jinmu12.com/",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36"
}


# ============== 工具函数 ==============
def get_local_ip():
    """获取本机IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def detect_environment():
    """检测运行环境"""
    is_mobile = False
    is_windows = False

    # 检测移动环境
    if hasattr(sys, 'getandroidapilevel'):
        is_mobile = True
    elif 'ANDROID_ROOT' in os.environ:
        is_mobile = True
    elif 'TERMUX_VERSION' in os.environ:
        is_mobile = True

    # 检测Windows
    if os.name == 'nt':
        is_windows = True

    return is_mobile, is_windows


def open_browser_auto(port, is_mobile=False):
    """自动打开浏览器（修复版：修正Termux环境检测）"""
    local_url = f"http://localhost:{port}"

    print(f"正在尝试打开浏览器: {local_url}")

    try:
        # 修复点：使用正确的环境变量名 'TERMUX_VERSION' 进行检测
        if is_mobile and ('TERMUX_VERSION' in os.environ):
            # Termux (Android) 环境
            print("✅ 检测到Termux环境，尝试调用 termux-open-url")
            # 执行命令，不捕获输出以便查看潜在错误
            result = subprocess.run(['termux-open-url', local_url],
                                    capture_output=False,  # 改为False，让错误信息直接显示
                                    shell=False,
                                    timeout=5)  # 设置超时
            # 由于 capture_output=False，成功执行即返回
            print("✅ 已向系统发送打开浏览器的请求")
            return True
        elif not is_mobile:
            # 桌面环境 (Windows, macOS, Linux)
            webbrowser.open(local_url)
            return True
        else:
            # 检测为移动环境但非Termux，或条件不满足，给出提示
            print(f"⚠️  当前环境可能不支持自动打开浏览器，请手动访问: {local_url}")
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  打开浏览器的请求超时，但可能已成功发送。请检查浏览器是否弹出。")
        return True
    except FileNotFoundError:
        print("❌ 未找到 'termux-open-url' 命令。请确保已在Termux中安装 'termux-api' 包。")
        print("   安装命令: pkg install termux-api")
        return False
    except Exception as e:
        print(f"❌ 自动打开浏览器时发生未知错误: {e}")
        print(f"   请手动在浏览器中访问: {local_url}")
        return False


# ============== 加密函数 ==============
def encrypt_password(password):
    """加密密码"""
    if not CRYPTO_AVAILABLE:
        return password  # 回退到不加密

    try:
        key_bytes = ENCRYPT_KEY.encode('utf-8').ljust(32, b'\x00')[:32]
        iv_bytes = ENCRYPT_IV.encode('utf-8').ljust(16, b'\x00')[:16]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        padded_data = pad(password.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        print(f"加密失败: {e}")
        return password


# ============== API函数 ==============
def send_sms_code_api(phone, area_code="0086"):
    """发送短信验证码"""
    if not REQUESTS_AVAILABLE:
        return False, "requests库未安装，无法发送验证码"

    data = {"user_mobile": phone, "type": 1, "area_code": area_code}
    try:
        response = requests.post(SMS_API, json=data, headers=HEADERS, timeout=10)
        result = response.json()
        return result.get("code") in ["1", 1], result.get("msg", "未知错误")
    except Exception as e:
        return False, f"网络请求失败: {str(e)}"


def register_user_api(phone, invite_code, password, sms_code, area_code="0086"):
    """注册账号"""
    if not REQUESTS_AVAILABLE:
        return False, "requests库未安装，无法注册"

    encrypted_password = encrypt_password(password)
    data = {
        "user_mobile": phone,
        "area_code": area_code,
        "code": sms_code,
        "password": encrypted_password,
        "registered_location": "1",
        "share_id": invite_code,
        "type": 1
    }
    try:
        response = requests.post(REGISTER_API, json=data, headers=HEADERS, timeout=10)
        result = response.json()
        if result.get("code") in ["1", 1]:
            return True, "注册成功"
        else:
            return False, result.get("msg", "注册失败")
    except Exception as e:
        return False, f"网络请求失败: {str(e)}"


# ============== HTTP请求处理器 ==============
class RegisterHandler(BaseHTTPRequestHandler):
    """处理HTTP请求"""

    # 修复编码问题的关键：重写send_response方法
    def send_response(self, code, message=None):
        """重写send_response以支持UTF-8编码"""
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = ''

        # 使用UTF-8编码消息
        if isinstance(message, str):
            message = message.encode('utf-8', 'replace').decode('latin-1')

        self.send_response_only(code, message)
        self.send_header('Server', 'Python-HTTP-Server')
        self.send_header('Date', self.date_time_string())

    def send_error(self, code, message=None, explain=None):
        """重写send_error以支持UTF-8编码"""
        try:
            # 使用UTF-8编码错误消息
            if message and isinstance(message, str):
                message = message.encode('utf-8', 'ignore').decode('latin-1')

            if explain and isinstance(explain, str):
                explain = explain.encode('utf-8', 'ignore').decode('latin-1')

            # 调用父类方法
            super().send_error(code, message, explain)
        except UnicodeEncodeError:
            # 如果仍然有编码错误，发送简单的英文错误
            super().send_error(code, "Page Not Found", None)

    def do_GET(self):
        """处理GET请求"""
        try:
            if self.path == '/' or self.path == '/index.html':
                self.send_html_page()
            elif self.path == '/api/invite_codes':
                self.send_invite_codes()
            elif self.path.startswith('/favicon.ico'):
                self.send_response(204)  # No Content
                self.end_headers()
            else:
                # 使用重写后的send_error
                self.send_error(404, "页面不存在")
        except Exception as e:
            self.send_error(500, f"服务器内部错误: {str(e)}")

    def do_POST(self):
        """处理POST请求"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
            else:
                data = {}

            if self.path == '/api/send_sms':
                self.handle_send_sms(data)
            elif self.path == '/api/register':
                self.handle_register(data)
            else:
                self.send_error(404, "API不存在")
        except json.JSONDecodeError:
            self.send_error(400, "请求数据格式错误")
        except Exception as e:
            self.send_error(500, f"处理请求时出错: {str(e)}")

    def send_html_page(self):
        """发送HTML页面"""
        # 生成邀请码选项
        options = ""
        for name, code in INVITE_CODES.items():
            options += f'<option value="{code}">{name}</option>'

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>金木注册工具</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, system-ui, sans-serif; padding: 20px; background: #f5f7fa; }}
        .container {{ max-width: 400px; margin: 0 auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 25px; font-size: 24px; }}
        .form-group {{ margin-bottom: 20px; }}
        label {{ display: block; margin-bottom: 8px; color: #34495e; font-weight: 500; font-size: 14px; }}
        input, select {{ width: 100%; padding: 12px 15px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; transition: border 0.3s; }}
        input:focus, select:focus {{ border-color: #3498db; outline: none; box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1); }}
        .code-group {{ display: flex; gap: 10px; }}
        .code-group input {{ flex: 3; }}
        .code-group button {{ flex: 2; white-space: nowrap; }}
        button {{ background: #3498db; color: white; border: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: 500; cursor: pointer; transition: background 0.3s; }}
        button:hover {{ background: #2980b9; }}
        button:disabled {{ background: #95a5a6; cursor: not-allowed; }}
        .result {{ margin-top: 20px; padding: 12px; border-radius: 8px; display: none; font-size: 14px; }}
        .success {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
        .error {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
        .status {{ text-align: center; margin-bottom: 20px; padding: 10px; background: #e8f4fc; border-radius: 8px; font-size: 13px; color: #3498db; }}
        .footer {{ text-align: center; margin-top: 20px; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>金木注册工具</h1>
        <div class="status" id="status">运行环境: 正常</div>

        <div class="form-group">
            <label>手机号</label>
            <input type="tel" id="phone" placeholder="请输入11位手机号" maxlength="11">
        </div>

        <div class="form-group">
            <label>邀请人</label>
            <select id="invite">{options}</select>
        </div>

        <div class="form-group">
            <label>密码</label>
            <input type="password" id="password" placeholder="至少6位密码">
        </div>

        <div class="form-group">
            <label>短信验证码</label>
            <div class="code-group">
                <input type="text" id="sms_code" placeholder="6位验证码" maxlength="6">
                <button onclick="sendSms()" id="sms_btn">获取验证码</button>
            </div>
        </div>

        <button onclick="register()" id="register_btn">开始注册</button>

        <div class="result" id="result"></div>
        <div class="footer"></div>
    </div>

    <script>
        let countdown = 0;
        let countdownTimer = null;

        async function sendSms() {{
            const phone = document.getElementById('phone').value;
            const btn = document.getElementById('sms_btn');

            if (!/^1[3-9]\\d{{9}}$/.test(phone)) {{
                showResult('请输入正确的手机号', false);
                return;
            }}

            btn.disabled = true;
            btn.textContent = '发送中...';

            try {{
                const response = await fetch('/api/send_sms', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ phone: phone }})
                }});

                const data = await response.json();
                showResult(data.message, data.success);

                if (data.success) {{
                    // 开始倒计时
                    countdown = 60;
                    startCountdown();
                }} else {{
                    btn.disabled = false;
                    btn.textContent = '获取验证码';
                }}
            }} catch (error) {{
                showResult('网络错误: ' + error.message, false);
                btn.disabled = false;
                btn.textContent = '获取验证码';
            }}
        }}

        function startCountdown() {{
            const btn = document.getElementById('sms_btn');

            if (countdownTimer) clearInterval(countdownTimer);

            countdownTimer = setInterval(() => {{
                if (countdown <= 0) {{
                    clearInterval(countdownTimer);
                    btn.disabled = false;
                    btn.textContent = '获取验证码';
                }} else {{
                    btn.textContent = `重新发送(${{countdown}}s)`;
                    countdown--;
                }}
            }}, 1000);
        }}

        async function register() {{
            const phone = document.getElementById('phone').value;
            const invite = document.getElementById('invite').value;
            const password = document.getElementById('password').value;
            const smsCode = document.getElementById('sms_code').value;
            const btn = document.getElementById('register_btn');

            if (!/^1[3-9]\\d{{9}}$/.test(phone)) {{
                showResult('请输入正确的手机号', false);
                return;
            }}

            if (password.length < 6) {{
                showResult('密码至少6位', false);
                return;
            }}

            if (!/^\\d{{6}}$/.test(smsCode)) {{
                showResult('请输入6位验证码', false);
                return;
            }}

            btn.disabled = true;
            const originalText = btn.textContent;
            btn.textContent = '注册中...';

            try {{
                const response = await fetch('/api/register', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        phone: phone,
                        invite_code: invite,
                        password: password,
                        sms_code: smsCode
                    }})
                }});

                const data = await response.json();
                showResult(data.message, data.success);

                if (data.success) {{
                    // 清空表单
                    document.getElementById('phone').value = '';
                    document.getElementById('password').value = '';
                    document.getElementById('sms_code').value = '';
                }}
            }} catch (error) {{
                showResult('网络错误: ' + error.message, false);
            }} finally {{
                btn.disabled = false;
                btn.textContent = originalText;
            }}
        }}

        function showResult(message, success) {{
            const resultEl = document.getElementById('result');
            resultEl.textContent = message;
            resultEl.className = 'result ' + (success ? 'success' : 'error');
            resultEl.style.display = 'block';

            // 5秒后隐藏
            setTimeout(() => {{
                resultEl.style.display = 'none';
            }}, 5000);
        }}

        // 页面加载时检查API状态
        window.onload = function() {{
            const statusEl = document.getElementById('status');
            if (!navigator.onLine) {{
                statusEl.textContent = '网络连接已断开，请检查网络';
                statusEl.style.background = '#f8d7da';
                statusEl.style.color = '#721c24';
            }}
        }};
    </script>
</body>
</html>'''

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(html.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def send_invite_codes(self):
        """返回邀请码列表"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(INVITE_CODES).encode('utf-8'))

    def handle_send_sms(self, data):
        """处理发送验证码请求"""
        phone = data.get('phone', '')

        if not phone or not phone.isdigit() or len(phone) != 11:
            self.send_json_response(False, "手机号格式错误")
            return

        if REQUESTS_AVAILABLE:
            success, message = send_sms_code_api(phone)
            self.send_json_response(success, message)
        else:
            self.send_json_response(True, f"模拟: 验证码已发送到 {phone} (未安装requests库)")

    def handle_register(self, data):
        """处理注册请求"""
        phone = data.get('phone', '')
        invite_code = data.get('invite_code', list(INVITE_CODES.values())[0])
        password = data.get('password', '')
        sms_code = data.get('sms_code', '')

        if not all([phone, password, sms_code]):
            self.send_json_response(False, "请填写完整信息")
            return

        if len(password) < 6:
            self.send_json_response(False, "密码至少6位")
            return

        if len(sms_code) != 6 or not sms_code.isdigit():
            self.send_json_response(False, "验证码格式错误")
            return

        if REQUESTS_AVAILABLE:
            success, message = register_user_api(phone, invite_code, password, sms_code)
            self.send_json_response(success, message)
        else:
            self.send_json_response(True, f"模拟: 用户 {phone} 注册成功 (未安装requests库)")

    def send_json_response(self, success, message, data=None):
        """发送JSON响应"""
        response = {
            "success": success,
            "message": message,
            "timestamp": time.time()
        }

        if data:
            response["data"] = data

        json_str = json.dumps(response, ensure_ascii=False)

        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(json_str.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(json_str.encode('utf-8'))

    def log_message(self, format, *args):
        """自定义日志输出格式"""
        # 禁用默认日志输出
        pass


# ============== 主程序 ==============
def main():
    """主程序入口"""
    is_mobile, is_windows = detect_environment()
    auto_open = '--no-browser' not in sys.argv

    print("=" * 60)
    print("金禾注册工具 - 通用版本")
    print(f"运行环境: {'手机' if is_mobile else '电脑'}{' (Windows)' if is_windows else ''}")
    print("=" * 60)

    # 检查依赖
    if not REQUESTS_AVAILABLE:
        print("警告: requests库未安装，API功能将不可用")
        print("安装命令: pip install requests")

    if not CRYPTO_AVAILABLE:
        print("警告: pycryptodome库未安装，加密功能将不可用")
        print("安装命令: pip install pycryptodome")

    # 尝试多个端口
    ports_to_try = [8080, 8081, 8888, 9000]
    server = None

    for port in ports_to_try:
        try:
            server_address = ('', port)
            server = HTTPServer(server_address, RegisterHandler)
            print(f"✓ 服务器已启动: http://localhost:{port}")

            local_ip = get_local_ip()
            if local_ip != "127.0.0.1":
                print(f"   网络地址: http://{local_ip}:{port} (同一网络可访问)")

            break
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"✗ 端口 {port} 被占用，尝试下一个端口...")
                continue
            else:
                raise

    if server is None:
        print("错误: 所有端口都被占用，无法启动服务器")
        return

    # 显示邀请码列表
    print("\n可用邀请人:")
    for i, (name, code) in enumerate(INVITE_CODES.items(), 1):
        print(f"  {i}. {name}: {code}")

    # 自动打开浏览器
    if auto_open:
        time.sleep(1)  # 等待服务器启动
        open_browser_auto(port, is_mobile)

    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"服务器错误: {e}")


# ============== 启动 ==============
if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)

    # 启动程序
    main()