FROM node:20 AS builder
WORKDIR /app

# Accept build arguments for public env vars
ARG NEXT_PUBLIC_LIVEKIT_URL
ARG NEXT_PUBLIC_API_URL

ENV NEXT_PUBLIC_LIVEKIT_URL=$NEXT_PUBLIC_LIVEKIT_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY package.json ./

# Set registry and use legacy-peer-deps to avoid resolution issues
RUN npm config set registry https://registry.npmjs.org/ &&     npm install --legacy-peer-deps

COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "start"]
