from flask import Flask, render_template, request
from prometheus_client import start_http_server, Gauge
import requests
import ssl
import socket
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)

# Prometheus metrics
UP_METRIC = Gauge('website_up', 'Is the website up?', ['website'])
SSL_EXPIRY_METRIC = Gauge('ssl_expiry_days', 'Days until SSL certificate expires', ['website'])

# Load websites from file
def load_websites():
    with open('websites.json') as f:
        return json.load(f)

websites = load_websites()

def check_website(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_ssl_expiry_date(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                ssl_info = ssock.getpeercert()
                expiry_date = ssl_info['notAfter']
                expiry_date = datetime.strptime(expiry_date, '%b %d %H:%M:%S %Y %Z')
                days_left = (expiry_date - datetime.utcnow()).days
                return days_left
    except Exception as e:
        return None

@app.route('/')
def index():
    for website in websites:
        status = 'Up' if check_website(website['url']) else 'Down'
        website['status'] = status
        UP_METRIC.labels(website=website['url']).set(1 if status == 'Up' else 0)

        hostname = website['url'].replace('https://', '').replace('http://', '').split('/')[0]
        days_left = get_ssl_expiry_date(hostname)
        if days_left is not None:
            website['ssl_expiry'] = f"{days_left} days"
            SSL_EXPIRY_METRIC.labels(website=website['url']).set(days_left)
        else:
            website['ssl_expiry'] = 'Unknown'
            SSL_EXPIRY_METRIC.labels(website=website['url']).set(float('nan'))

    return json.dumps(websites)

@app.route('/metrics')
def metrics():
    return app.response_class(start_http_server(8000), content_type='text/plain')

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(8000)
    # Start Flask app
    app.run(host='0.0.0.0', port=5000)
