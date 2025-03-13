# Стадия 1: Сборка приложения
FROM node:18-alpine AS build

# Передача переменных окружения через ARG
ARG REACT_APP_API_BASE_URL
ENV REACT_APP_API_BASE_URL=${REACT_APP_API_BASE_URL}

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json (если есть)
COPY package*.json ./

# Установка зависимостей
RUN npm install --silent

# Копирование исходного кода приложения
COPY . .

# Сборка приложения в production-режиме
RUN npm run build

# Стадия 2: Подготовка production-образа
FROM node:18-alpine

# Установка serve для обслуживания статических файлов
RUN npm install -g serve

# Создание директории для статических файлов
WORKDIR /usr/src/app

# Копирование собранного приложения из первой стадии
COPY --from=build /app/build ./build

# Открытие порта
EXPOSE 3000

# Запуск сервера serve
CMD ["serve", "-s", "build", "-l", "3000"]