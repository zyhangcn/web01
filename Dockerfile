FROM reg2.hypers.cc/library/python/python-slim:base
ENV DJANGO_SETTINGS_MODULE=management.settings
ADD . /app
WORKDIR /app
RUN pip install --no-cache-dir --trusted-host mirrors.aliyun.com/pypi/simple --index-url
http://mirrors.aliyun.com/pypi/simple -r requirement.txt
CMD ["/app/run.sh"]

