FROM node:16 AS build

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .

# RUN if [ "$IS_PRODUCTION" = "true" ]; then npm run build; else npm run serve; fi
CMD ["npm", "run", "serve"]
