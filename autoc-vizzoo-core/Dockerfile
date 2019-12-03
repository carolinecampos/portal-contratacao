FROM gitlab-dreg.nexxera.com/devops/dockerimages/python-oracle:3.6-debian8-slim

LABEL maintainer="Nexxera DevOps "devops@nexxera.com""

COPY ./autoc_vizzoo/. /app
COPY requirements.txt /app
WORKDIR /app

RUN chmod -R g+rw /app \    
    && pip install -r requirements.txt \
    && chmod +x /app/run.sh

CMD ["/app/run.sh"]
