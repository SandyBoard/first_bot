FROM python:3.11.4-alpine3.18
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY bot.py tk.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "bot.py"]
