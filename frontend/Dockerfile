FROM node:latest as build-stage

RUN mkdir -p /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
RUN npm install --global @vue/cli
RUN npm install -g @vue/cli-service-global
RUN git clone https://github.com/CubicrootXYZ/Parlismonitoring.git /tmp/app
RUN cp /tmp/app/frontend/nginx.conf /tmp/nginx.conf
RUN mv /tmp/app/frontend/.eslintrc.js /usr/src/app/.eslintrc.js
RUN mv /tmp/app/frontend/* /usr/src/app
RUN rm -R /tmp/app
RUN rm -rf /usr/src/app/node_modules
RUN ls /usr/src/app
RUN cd /usr/src/app && npm install
RUN cd /usr/src/app && npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /usr/src/app /app
RUN ls /tmp
COPY --from=build-stage /tmp/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]