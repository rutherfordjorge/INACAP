const SESSION_KEY = 'office365_demo_user';
const demoUser = {
  username: 'usuario@office365.com',
  password: 'inacap123',
  displayName: 'Usuario Office 365',
};

export function authenticate(username, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const normalizedUser = username.trim().toLowerCase();
      const isValid =
        normalizedUser === demoUser.username.toLowerCase() && password === demoUser.password;

      if (isValid) {
        const session = { username: demoUser.username, displayName: demoUser.displayName };
        sessionStorage.setItem(SESSION_KEY, JSON.stringify(session));
        resolve(session);
      } else {
        reject(new Error('Credenciales de Office 365 inválidas.'));
      }
    }, 350);
  });
}

export function signOut() {
  sessionStorage.removeItem(SESSION_KEY);
}

export function restoreSession() {
  const savedSession = sessionStorage.getItem(SESSION_KEY);
  if (!savedSession) return null;

  try {
    return JSON.parse(savedSession);
  } catch (error) {
    sessionStorage.removeItem(SESSION_KEY);
    return null;
  }
}
