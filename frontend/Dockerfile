FROM node:16

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . .

ENV RUN_MODE=serve

CMD npm run $RUN_MODE
