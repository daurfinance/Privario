// webapp/src/components/Balance.jsx

import React from "react";

export default function Balance({ amount }) {
  return (
    <div className="mb-4">
      <p className="text-sm text-gray-400">Баланс</p>
      <p className="text-2xl font-bold">${amount.toFixed(2)}</p>
    </div>
  );
}
