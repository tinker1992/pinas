from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# 定义 HTML 模板，包含两个按钮
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Control</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-family: Arial, sans-serif;
            margin-top: 50px;
        }
        h1 {
            font-size: 2rem;
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            gap: 25px;
        }
        button {
            width: 150px;
            padding: 15px;
            font-size: 1.2rem;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #45a049;
        }
        button:active {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <h1>Server Control</h1>
    <div class="button-container">
        <form method="POST" action="/shutdown">
            <button type="submit">Shutdown</button>
        </form>
        <form method="POST" action="/reboot">
            <button type="submit">Reboot</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # 渲染包含按钮的 HTML 页面
    return render_template_string(html_template)

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        # 执行系统关机命令
        os.system('/sbin/shutdown now')
        return "Server is shutting down...", 200
    except Exception as e:
        return f"Failed to shutdown: {str(e)}", 500

@app.route('/reboot', methods=['POST'])
def reboot():
    try:
        # 执行系统重启命令
        os.system('/sbin/reboot now')
        return "Server is rebooting...", 200
    except Exception as e:
        return f"Failed to reboot: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
