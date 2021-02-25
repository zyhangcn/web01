FROM reg2.hypers.cc/library/python/python-slim:base
ENV DJANGO_SETTINGS_MODULE=management.settings
ADD . /app
WORKDIR /app
RUN pip  install -r requirement.txt
CMD ["/app/run.sh"]

