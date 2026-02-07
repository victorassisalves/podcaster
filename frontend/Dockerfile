FROM node:18-slim AS builder
WORKDIR /app

# Accept build arguments for public env vars
ARG NEXT_PUBLIC_LIVEKIT_URL
ARG NEXT_PUBLIC_API_URL

ENV NEXT_PUBLIC_LIVEKIT_URL=$NEXT_PUBLIC_LIVEKIT_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-slim
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "start"]
