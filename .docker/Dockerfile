FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -la

EXPOSE 8000

# CMD ["uvicorn", "pyfolio.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
CMD ["/usr/src/app/.docker/start.sh"]
