FROM svizor/zoomcamp-model:mlops-3.10.0-slim

# RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system  -ignore-pipfile
RUN pipenv sync --system

COPY [ "scripts/starter.py", "./" ]

ENTRYPOINT [ "python", "starter.py" ]
# ENTRYPOINT [ "bash" ]

# pipenv run docker build -t hw4-q6-mean-duration-prediction:v1 .
# pipenv run docker run -it hw4-q6-mean-duration-prediction:v1 --year 2022 --month 4