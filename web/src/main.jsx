import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

import {
  api,
  hasSession,
  login,
  logout,
} from "./api";

import DashboardLayout from "./layouts/DashboardLayout";
import Header from "./components/Header";
import Dashboard from "./features/dashboard/Dashboard";
import AIAssistant from "./features/assistant/AIAssistant";

import "./styles.css";
import "./auth.css";


function Login({ onSuccess }) {
  const [u, setU] = useState("director");
  const [p, setP] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");

    try {
      await login(u, p);
      onSuccess();
    } catch (x) {
      setError(x.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <main className="loginPage" dir="rtl">
      <form className="loginCard" onSubmit={submit}>
        <div className="loginMark">PG</div>
        <small>POSTGRADUATE STUDIES</small>

        <h1>تسجيل الدخول</h1>

        <p>
          منظومة إدارة الدراسات العليا – كلية الطب
        </p>

        <label>
          اسم المستخدم
          <input
            value={u}
            onChange={(e)=>setU(e.target.value)}
          />
        </label>

        <label>
          كلمة المرور
          <input
            type="password"
            value={p}
            onChange={(e)=>setP(e.target.value)}
          />
        </label>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        <button disabled={busy}>
          {busy ? "جارٍ التحقق..." : "دخول آمن"}
        </button>

      </form>
    </main>
  );
}


function DashboardPage(){

  const [user,setUser] = useState(null);
  const [data,setData] = useState(null);
  const [lang,setLang] = useState("ar");
  const [error,setError] = useState("");

  useEffect(()=>{
    Promise.all([
      api("/me/"),
      api("/dashboard/")
    ])
    .then(([me,d])=>{
      setUser(me);
      setLang(me.language || "ar");
      setData(d);
    })
    .catch(e=>setError(e.message));

  },[]);


  if(error){
    return (
      <div className="fatal" dir="rtl">
        <h2>تعذر تحميل النظام</h2>
        <p>{error}</p>

        <button onClick={()=>{
          logout();
          location.reload();
        }}>
          العودة لتسجيل الدخول
        </button>

      </div>
    );
  }


  if(!user || !data){
    return (
      <div className="loading" dir="rtl">
        جارٍ تحميل لوحة التحكم…
      </div>
    );
  }


  return (
    <DashboardLayout
      user={user}
      language={lang}
      onLanguageChange={()=>{
        setLang(
          lang === "ar" ? "en" : "ar"
        );
      }}
      onLogout={()=>{
        logout();
        location.reload();
      }}
    >

      <Header
        user={user}
        language={lang}
        onLanguageChange={()=>{
          setLang(
            lang === "ar" ? "en" : "ar"
          );
        }}
        onLogout={()=>{
          logout();
          location.reload();
        }}
      />

      <Dashboard data={data}/>

      <AIAssistant api={api}/>

    </DashboardLayout>
  );
}



function App(){

  const [
    authenticated,
    setAuthenticated
  ] = useState(hasSession());


  return authenticated
    ? <DashboardPage/>
    : <Login onSuccess={()=>setAuthenticated(true)}/>;

}


createRoot(
  document.getElementById("root")
)
.render(
  <App/>
);
