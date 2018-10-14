FROM dantup/unicorn_hd
WORKDIR /root/app/

RUN pip install websockets jsonrpcserver
COPY ./server.py .

ENTRYPOINT ["python", "-u", "server.py"]
