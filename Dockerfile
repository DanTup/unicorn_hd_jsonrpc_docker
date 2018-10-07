FROM dantup/unicorn_hd_demo
WORKDIR /root/app/

RUN pip install websockets jsonrpcserver
COPY ./server.py .

ENTRYPOINT ["python", "-u", "server.py"]
