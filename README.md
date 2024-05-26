Python application that monitors website uptime and SSL certificate expiry, exposes metrics for Prometheus, and uses a separate file for website URLs. This application is also Dockerized.

1. Directory Structure
Create the following directory structure:

website_monitor/
│
├── Dockerfile
├── website_monitor.py
├── websites.json
└── requirements.txt
2. website_monitor.py
This is the main application script.

3. websites.json
This file contains the list of websites to monitor.


4. requirements.txt
This file lists the dependencies required for the application.

Run the Docker container:

docker run -p 5000:5000 -p 8000:8000 website-monitor

7. Accessing the Application

Open your web browser and navigate to http://localhost:5000 to see the status of the websites in JSON format.
The Prometheus metrics will be available at http://localhost:8000/metrics.

8. Configuring Prometheus

To scrape the metrics from this application, add the following job to your Prometheus configuration file (prometheus.yml):

scrape_configs:
  - job_name: 'website_monitor'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']

This setup allows you to monitor website uptime, SSL certificate expiry, manage the list of websites via a JSON file, and expose metrics for Prometheus. The application is also Dockerized for easy deployment.
