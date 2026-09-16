from flask import Flask
from collections import Counter

app = Flask(__name__)
def load_devices(path="devices.txt"):
    devices = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                name, ip = line.split()
                devices.append((name, ip))
    return devices

def find_duplicates(devices):
    counts = Counter(ip for _, ip in devices)
    return sorted(ip for ip, n in counts.items() if n > 1)

@app.route("/")
def index():
    devices = load_devices()
    dupes = find_duplicates(devices)
    rows = "".join(f"<tr><td>{n}</td><td>{ip}</td></tr>" for n, ip in devices)
    if dupes:
        status = f"<p style='color:red'>FAIL - duplicate IP(s): {', '.join(dupes)}</p>"
    else:
        status = "<p style='color:green'>PASS - all device IPs are unique</p>"
    return f"<h1>CNIT 381 IP Checker</h1>{status}<table border='1'>{rows}</table>"
@app.route("/check")
def check():
    dupes = find_duplicates(load_devices())
    return {"duplicates": dupes, "ok": len(dupes) == 0}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)