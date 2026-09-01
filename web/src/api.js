const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
let accessToken = localStorage.getItem('pgms_access');
let refreshToken = localStorage.getItem('pgms_refresh');
export async function login(username,password){const r=await fetch(`${API_URL}/auth/token/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});if(!r.ok)throw new Error('اسم المستخدم أو كلمة المرور غير صحيحة');const t=await r.json();accessToken=t.access;refreshToken=t.refresh;localStorage.setItem('pgms_access',accessToken);localStorage.setItem('pgms_refresh',refreshToken)}
async function refreshAccess(){if(!refreshToken)return false;const r=await fetch(`${API_URL}/auth/refresh/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh:refreshToken})});if(!r.ok)return false;accessToken=(await r.json()).access;localStorage.setItem('pgms_access',accessToken);return true}
export async function api(path,options={},retry=true){const r=await fetch(`${API_URL}${path}`,{...options,headers:{...options.headers,'Content-Type':'application/json',Authorization:`Bearer ${accessToken}`}});if(r.status===401&&retry&&await refreshAccess())return api(path,options,false);if(!r.ok)throw new Error((await r.json()).error||'تعذر الاتصال بالخادم');return r.json()}
export function hasSession(){return Boolean(accessToken&&refreshToken)}
export function logout(){accessToken=null;refreshToken=null;localStorage.removeItem('pgms_access');localStorage.removeItem('pgms_refresh')}
