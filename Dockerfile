FROM dantup/unicorn_hd_demo
WORKDIR /root/app/

RUN pip install websockets jsonrpcserver
COPY ./server.py .

# TODO: Allow passing port, keep-on, rotation settings
CMD ["server.py"]
ENTRYPOINT ["python"]
