// webapp/src/components/Card.jsx

import React from "react";

export default function Card({ name, number, exp, cvc }) {
  return (
    <div className="bg-gradient-to-br from-[#1a1a1d] to-[#27272a] p-6 rounded-2xl shadow-xl my-6">
      <p className="text-lg font-bold tracking-widest">{number}</p>
      <div className="flex justify-between mt-4">
        <div>
          <p className="text-xs text-gray-400">VALID THRU</p>
          <p className="text-sm">{exp}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">CVC</p>
          <p className="text-sm">{cvc}</p>
        </div>
      </div>
      <p className="mt-4 text-base font-semibold uppercase">{name}</p>
    </div>
  );
}
