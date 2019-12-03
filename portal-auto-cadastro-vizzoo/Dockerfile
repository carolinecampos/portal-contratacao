FROM gitlab-dreg.nexxera.com/devops/dockerimages/nginx:1.12.0-alpine3.6

COPY ./portal-auto-cadastro-vizzoo/dist/portal-auto-cadastro-vizzoo/* /app/
COPY ./portal-auto-cadastro-vizzoo/run.sh /run.sh
COPY ./portal-auto-cadastro-vizzoo/environment/nginx.vh.default.conf /etc/nginx/conf.d/default.conf

RUN chmod +x /run.sh

CMD ["/run.sh"]
