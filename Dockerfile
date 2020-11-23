FROM python:3-alpine AS compile-image
RUN apk add build-base

RUN addgroup -S liveproxy && adduser -S liveproxy -G liveproxy
USER liveproxy

RUN pip install --user --no-cache-dir --no-warn-script-location liveproxy


FROM python:3-alpine AS runtime-image

RUN addgroup -S liveproxy && adduser -S liveproxy -G liveproxy
USER liveproxy
COPY --from=compile-image /home/liveproxy/.local /home/liveproxy/.local
RUN mkdir -p /home/liveproxy/.config/streamlink/plugins
ENV PATH=/home/liveproxy/.local/bin:$PATH

EXPOSE 53422

ENTRYPOINT [ "liveproxy" ]