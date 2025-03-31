import React, { useEffect, useState } from "react";
import { TonConnectButton } from "@tonconnect/ui-react";
import { useTranslation } from "react-i18next";
import axios from "axios";

const API = "http://localhost:8000/api"; // при деплое укажи свой backend URL

export default function App() {
  const [user, setUser] = useState(null);
  const [balance, setBalance] = useState(null);
  const { t, i18n } = useTranslation();
  const tg = window.Telegram.WebApp;

  useEffect(() => {
    tg.ready();
    tg.expand();
    const id = tg.initDataUnsafe?.user?.id || "7155546894";
    axios.get(`${API}/user-info?user_id=${id}`).then((res) => {
      setUser(res.data);
    });
    axios.get(`${API}/get-balance?user_id=${id}`).then((res) => {
      setBalance(res.data);
    });
  }, []);

  const changeLanguage = (lang) => {
    i18n.changeLanguage(lang);
  };

  const handleTransfer = async () => {
    const id = tg.initDataUnsafe?.user?.id;
    await axios.post(`${API}/transfer`, {
      sender_id: id,
      to_type: "card",
      recipient: "demo",
      amount: 10
    });
    alert("✅ Переведено $10!");
  };

  if (!user || !balance) return <div className="text-white p-4">Загрузка...</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-2xl font-bold mb-4">{t("welcome")}, {user.name}!</h1>

      <div className="mb-4 space-y-2">
        <p>💳 {t("card_balance")}: ${balance.card_balance}</p>
        <p>🪙 TRON: {balance.tron_balance} USDT</p>
        <p>💎 TON: {balance.ton_balance} TON</p>
      </div>

      <div className="space-y-2">
        <button className="bg-blue-600 w-full py-2 rounded" onClick={handleTransfer}>
          🔁 {t("send")} $10
        </button>

        <button className="bg-yellow-500 w-full py-2 rounded" onClick={() => changeLanguage("ru")}>🇷🇺 Русский</button>
        <button className="bg-green-600 w-full py-2 rounded" onClick={() => changeLanguage("kz")}>🇰🇿 Қазақ</button>
        <button className="bg-gray-700 w-full py-2 rounded" onClick={() => changeLanguage("en")}>🇬🇧 English</button>

        <TonConnectButton className="mt-4" />
      </div>
    </div>
  );
}
