# ---- Build stage ----
FROM node:20-alpine AS builder

RUN corepack enable

WORKDIR /build

COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile 2>/dev/null || npm install

COPY . .
RUN npm run build

# ---- Runtime stage ----
FROM nginx:alpine AS runtime

COPY --from=builder /build/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
