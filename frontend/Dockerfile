FROM node:16

WORKDIR /frontend

COPY . .

RUN npm install

ENV PORT=8081

CMD ["npm", "run", "serve"]
