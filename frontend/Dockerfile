FROM node:20 AS build-stage

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

FROM node:20-alpine AS production-stage

WORKDIR /app

COPY --from=build-stage /app/.output /app/.output
COPY --from=build-stage /app/package*.json ./

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]