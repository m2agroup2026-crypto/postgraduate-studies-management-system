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
          مركز قيادة الدراسات العليا
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
          <b>{user?.name}</b>
          <small>{user?.title}</small>
        </div>
      </div>
    </header>
  );
}
