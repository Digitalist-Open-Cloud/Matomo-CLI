FROM python:3.12.6-alpine
RUN pip install matomo-cli==0.1.5 --no-cache-dir
CMD ["python", "/usr/local/lib/python3.12/site-packages/matomo_cli/prometheus.py" ]
