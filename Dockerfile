FROM python:3
WORKDIR /workdir
COPY . .
RUN pip install --upgrade pip && pip install \
    black \
    flake8 \
    mutmut \
    mypy \
    pandas-stubs \
    pylint \
    pytest \
    pytest-cov
RUN pip3 install -r requirements.txt

EXPOSE 8501
