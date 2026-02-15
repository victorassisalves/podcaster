FROM node:18-slim AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
# Use npm ci for deterministic installs
RUN npm ci

# Copy source code
COPY . .

# Build arguments for Next.js static generation
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_LIVEKIT_URL

# Set environment variables for the build process
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_LIVEKIT_URL=$NEXT_PUBLIC_LIVEKIT_URL

# Build the application
RUN npm run build

# Ensure public directory exists
RUN mkdir -p public

# Production image
FROM node:18-slim AS runner

WORKDIR /app

ENV NODE_ENV=production

# Copy necessary files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["npm", "start"]
