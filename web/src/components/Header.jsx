import React from "react";
import { Languages, LogOut } from "lucide-react";

export default function Header({
  user,
  language,
  onLanguageChange,
  onLogout,
}) {
  const ar = language === "ar";

  return (
    <header>
      <div>
        <small>
          Postgraduate Studies Management System
        </small>

        <h1>
          {ar ? "مركز قيادة الدراسات العليا" : "Postgraduate Studies Command Center"}
        </h1>
      </div>

      <div className="actions">
        <button onClick={onLanguageChange}>
          <Languages size={18} />
          {ar ? "English" : "العربية"}
        </button>

        <button
          className="logout"
          onClick={onLogout}
        >
          <LogOut size={18} />
        </button>

        <div className="profile">
          <b>
            {ar ? user?.name : "Prof. Dr. Mohamed Abdel Baset Khalaf"}
          </b>
          <small>
            {ar ? user?.title : "Vice Dean for Postgraduate Studies and Research"}
          </small>
        </div>
      </div>
    </header>
  );
}
