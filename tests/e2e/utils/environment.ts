export const testEnvironment = {
  baseURL: process.env.PGMS_WEB_URL || 'http://localhost:5173',
  apiURL: process.env.PGMS_API_URL || 'http://localhost:8000/api/v1'
};
