// webapp/src/components/Buttons.jsx

import React from "react";

export default function Buttons({ setBalance }) {
  return (
    <div className="flex flex-col gap-4 mt-6">
      <button
        onClick={() => setBalance((b) => b + 100)}
        className="bg-blue-600 py-2 rounded-xl hover:bg-blue-700 transition"
      >
        Пополнить
      </button>
      <button
        onClick={() => setBalance((b) => b - 50)}
        className="bg-purple-600 py-2 rounded-xl hover:bg-purple-700 transition"
      >
        Перевести
      </button>
      <button className="bg-gray-700 py-2 rounded-xl hover:bg-gray-600 transition">
        История
      </button>
    </div>
  );
}
