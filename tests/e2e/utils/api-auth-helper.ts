export interface AuthUser {
  username: string;
  password: string;
}

export async function authenticateUser(request: any, user: AuthUser) {
  const response = await request.post('/api/v1/auth/login/', {
    data: user,
  });

  return response;
}
