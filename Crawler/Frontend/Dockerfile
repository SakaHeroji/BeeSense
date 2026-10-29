FROM node:22-alpine@sha256:fe4f6d74e20370acb04ad889077d14d0f64a9c8ea6a42bc60cddf1e844699914 AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
ARG VITE_DATA_MODE=api
ARG VITE_API_BASE_URL=/api/v1
ARG VITE_PROJECT_ID=university-intelligence
ARG VITE_NLP_URL=
ARG VITE_DASHBOARD_URL=
ENV VITE_DATA_MODE=${VITE_DATA_MODE} VITE_API_BASE_URL=${VITE_API_BASE_URL} VITE_PROJECT_ID=${VITE_PROJECT_ID} VITE_NLP_URL=${VITE_NLP_URL} VITE_DASHBOARD_URL=${VITE_DASHBOARD_URL}
RUN npm run build

FROM nginxinc/nginx-unprivileged:stable-alpine@sha256:f5116ed4606f3eb015dd4a8e28cb9b351476dc0ad4bc6e9f93b19cec130cdf03
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
USER 101
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
