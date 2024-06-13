FROM alpine:latest

# Install Python and pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update python3 py3-pip
RUN rm /usr/lib/python*/EXTERNALLY-MANAGED && \
    python3 -m ensurepip
RUN apk add python3-dev

# Install gcc
RUN apk add build-base
RUN apk add unixodbc-dev

WORKDIR /app
COPY . .

# Install curl
RUN apk add --update \
    curl \
    && rm -rf /var/cache/apk/*

# Install gpg
RUN apk update \
    && apk fetch gnupg \
    && apk add gnupg \
    && gpg --list-keys



# Install Azure ODBC
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.3.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.apk
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/msodbcsql18_18.3.3.1-1_amd64.sig
RUN curl -O https://download.microsoft.com/download/3/5/5/355d7943-a338-41a7-858d-53b259ea33f5/mssql-tools18_18.3.1.1-1_amd64.sig

RUN find ~/.gnupg -name '*.lock' -delete
RUN curl https://packages.microsoft.com/keys/microsoft.asc  | gpg --import -

RUN find ~/.gnupg -name '*.lock' -delete
RUN gpg --verify msodbcsql18_18.3.3.1-1_amd64.sig msodbcsql18_18.3.3.1-1_amd64.apk

RUN find ~/.gnupg -name '*.lock' -delete
RUN gpg --verify mssql-tools18_18.3.1.1-1_amd64.sig mssql-tools18_18.3.1.1-1_amd64.apk
RUN apk add --allow-untrusted msodbcsql18_18.3.3.1-1_amd64.apk
RUN apk add --allow-untrusted mssql-tools18_18.3.1.1-1_amd64.apk

EXPOSE 8000
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

