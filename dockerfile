FROM python:3.7-alpine

ADD symbol_check.py /
ADD run_symbol_check /etc/periodic/hourly
ADD config.ini /
ADD crontab /

RUN pip3 install requests
RUN chmod +x /etc/periodic/hourly/run_symbol_check

#ENTRYPOINT [ "python3.7", "symbol_check.py" ]
CMD ["crond", "-f"]
