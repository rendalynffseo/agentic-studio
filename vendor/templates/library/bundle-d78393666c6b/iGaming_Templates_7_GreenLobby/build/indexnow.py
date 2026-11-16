"""IndexNow: tell Bing, Yandex, Seznam, Naver etc. about new/updated pages right after a deploy.

  python3 build/indexnow.py key      create the key once (build/.indexnow_key) and write <key>.txt to the site root
  python3 build/indexnow.py submit   submit every URL in dist/sitemap.xml (run AFTER the deploy is live)

The key file must be reachable at https://<domain>/<key>.txt, so deploy it with the site.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_STORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".indexnow_key")
ENDPOINT = "https://api.indexnow.org/indexnow"


def ensure_key():
    if os.path.exists(KEY_STORE):
        key = open(KEY_STORE).read().strip()
    else:
        key = uuid.uuid4().hex
        with open(KEY_STORE, "w") as fh:
            fh.write(key)
    for f in os.listdir(ROOT):  # keep exactly one key file in the root
        if re.fullmatch(r"[0-9a-f]{32}\.txt", f) and f != f"{key}.txt":
            os.remove(os.path.join(ROOT, f))
    with open(os.path.join(ROOT, f"{key}.txt"), "w") as fh:
        fh.write(key)
    return key


def submit():
    key = ensure_key()
    urls = re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "dist", "sitemap.xml")).read())
    if not urls:
        sys.exit("no URLs in sitemap.xml")
    host = urlparse(urls[0]).netloc
    body = json.dumps({"host": host, "key": key, "keyLocation": f"https://{host}/{key}.txt", "urlList": urls}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
    except urllib.error.HTTPError as err:
        code = err.code
    meaning = {200: "OK", 202: "accepted (key will be validated)", 400: "bad request", 403: "key not valid / key file not found",
               422: "URLs don't match host or key", 429: "too many requests"}.get(code, "")
    print(f"IndexNow: {len(urls)} URLs for {host} -> HTTP {code} {meaning}")
    return code in (200, 202)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "key"
    if cmd == "key":
        print(ensure_key())
    elif cmd == "submit":
        sys.exit(0 if submit() else 1)
    else:
        sys.exit(__doc__)
