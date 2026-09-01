import * as SecureStore from 'expo-secure-store';
const API_URL=process.env.EXPO_PUBLIC_API_URL||'http://10.0.2.2:8000/api/v1';
export async function login(username,password){const r=await fetch(`${API_URL}/auth/token/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username,password})});if(!r.ok)throw new Error('بيانات الدخول غير صحيحة');const t=await r.json();await SecureStore.setItemAsync('access',t.access);await SecureStore.setItemAsync('refresh',t.refresh)}
export async function api(path,options={}){const token=await SecureStore.getItemAsync('access');const r=await fetch(`${API_URL}${path}`,{...options,headers:{...options.headers,'Content-Type':'application/json',Authorization:`Bearer ${token}`}});if(!r.ok)throw new Error('تعذر الاتصال بالخادم');return r.json()}
export async function hasSession(){return Boolean(await SecureStore.getItemAsync('access'))}
export async function logout(){await SecureStore.deleteItemAsync('access');await SecureStore.deleteItemAsync('refresh')}
