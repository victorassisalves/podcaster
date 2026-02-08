FROM node:20-slim AS builder
WORKDIR /app

# Accept build arguments for public env vars
ARG NEXT_PUBLIC_LIVEKIT_URL
ARG NEXT_PUBLIC_API_URL

ENV NEXT_PUBLIC_LIVEKIT_URL=$NEXT_PUBLIC_LIVEKIT_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package.json ./
# Use --prefer-online to help with potential registry issues
RUN npm install --prefer-online

COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "start"]
