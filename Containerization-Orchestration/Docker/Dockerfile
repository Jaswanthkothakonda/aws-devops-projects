FROM amazonlinux:2023
RUN dnf install -y nginx && \
    dnf clean all
WORKDIR /usr/share/nginx/html
COPY index.html .
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]



