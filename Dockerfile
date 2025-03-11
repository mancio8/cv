# Stage 1: Build Stage
FROM node:lts AS builder
WORKDIR /app

# Copy package.json and package-lock.json for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app source code
COPY . .

# Build the Astro project
RUN npm run build

# Stage 2: Production Stage
FROM node:lts AS runtime
WORKDIR /app

# Copy the build output from the builder stage
COPY --from=builder /app/dist /app/dist

# Expose the port Astro uses
EXPOSE 4321

# Start the Astro server
CMD ["npx", "astro", "preview"]
