// webapp/src/i18n.js

import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  ru: {
    translation: {
      welcome: "Добро пожаловать",
      balance: "Баланс",
      deposit: "Пополнить",
      transfer: "Перевести",
      history: "История",
    }
  },
  kz: {
    translation: {
      welcome: "Қош келдіңіз",
      balance: "Баланс",
      deposit: "Толықтыру",
      transfer: "Аудару",
      history: "Тарих",
    }
  },
  en: {
    translation: {
      welcome: "Welcome",
      balance: "Balance",
      deposit: "Deposit",
      transfer: "Transfer",
      history: "History",
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: "ru",
    fallbackLng: "en",
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
