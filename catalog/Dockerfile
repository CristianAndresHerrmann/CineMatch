# Stage 1: Build stage
FROM node:20-alpine AS builder

# Instalar pnpm usando corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copiar archivos de configuración
COPY package.json pnpm-lock.yaml* ./

# Instalar todas las dependencias
RUN pnpm install --frozen-lockfile

# Copiar código fuente
COPY src/ ./src/
COPY tsconfig.json ./

# Compilar TypeScript
RUN pnpm run build

# Stage 2: Production stage
FROM node:20-alpine AS production

# Instalar pnpm para poder usar scripts
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copiar package.json y lock file
COPY package.json pnpm-lock.yaml* ./

# Instalar solo dependencias de producción
RUN pnpm install --prod --frozen-lockfile

# Instalar mínimas dev dependencies necesarias para seeding
RUN pnpm add typescript ts-node-dev dotenv --save-dev

# Copiar código compilado desde build stage
COPY --from=builder /app/dist ./dist

# Copiar código fuente para seeding (necesario para ts-node-dev)
COPY src/ ./src/
COPY tsconfig.json ./

# Crear usuario no root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodeuser -u 1001

# Cambiar propiedad y cambiar a usuario no root
RUN chown -R nodeuser:nodejs /app
USER nodeuser

# Exponer puerto
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3001/health || exit 1

# Comando por defecto
CMD ["node", "dist/index.js"]