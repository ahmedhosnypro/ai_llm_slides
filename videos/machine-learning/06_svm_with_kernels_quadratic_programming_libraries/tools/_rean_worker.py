
import base64, json, sys, urllib.request
img, prompt, out, mt = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
key = open(sys.argv[5]).read().strip()
with open(img, "rb") as f:
    url = "data:image/png;base64," + base64.b64encode(f.read()).decode()
payload = {"model": "images", "max_tokens": mt, "stream": True,
           "thinking": {"type": "disabled"},
           "messages": [{"role": "user", "content": [
               {"type": "text", "text": prompt},
               {"type": "image_url", "image_url": {"url": url}}]}]}
req = urllib.request.Request("http://localhost:17844/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
total = 0
with open(out, "w") as f, urllib.request.urlopen(req, timeout=int(sys.argv[6])) as r:
    for line in r:
        line = line.decode("utf-8", "replace").strip()
        if not line.startswith("data:"):
            continue
        d = line[5:].strip()
        if d == "[DONE]":
            break
        try:
            c = json.loads(d)["choices"][0]["delta"].get("content")
        except Exception:
            c = None
        if c:
            f.write(c)
            f.flush()
            total += len(c)
print("banked", total)
