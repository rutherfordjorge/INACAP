import { createAlertBanner } from '../../components/feedback/alertBanner.js';
import { authenticate } from '../../services/auth/office365Auth.js';

export function createLoginView({ onSuccess }) {
  const container = document.createElement('section');
  container.className = 'card login-view';

  const title = document.createElement('h1');
  title.textContent = 'Accede con Office 365';

  const description = document.createElement('p');
  description.textContent = 'Ingresa tus credenciales institucionales para continuar.';

  const form = document.createElement('form');
  form.className = 'login-form';

  const userField = document.createElement('input');
  userField.type = 'email';
  userField.name = 'username';
  userField.placeholder = 'usuario@office365.com';
  userField.required = true;

  const passwordField = document.createElement('input');
  passwordField.type = 'password';
  passwordField.name = 'password';
  passwordField.placeholder = 'Contraseña';
  passwordField.required = true;

  const submitButton = document.createElement('button');
  submitButton.type = 'submit';
  submitButton.textContent = 'Ingresar';

  const feedbackSlot = document.createElement('div');
  feedbackSlot.className = 'feedback-slot';

  form.appendChild(userField);
  form.appendChild(passwordField);
  form.appendChild(submitButton);
  form.appendChild(feedbackSlot);

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    feedbackSlot.innerHTML = '';
    submitButton.disabled = true;
    submitButton.textContent = 'Validando...';

    try {
      const session = await authenticate(userField.value, passwordField.value);
      feedbackSlot.appendChild(
        createAlertBanner({ type: 'success', message: 'Inicio de sesión exitoso.' })
      );
      onSuccess?.(session);
    } catch (error) {
      feedbackSlot.appendChild(
        createAlertBanner({ type: 'error', message: error.message ?? 'Error de autenticación' })
      );
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = 'Ingresar';
    }
  });

  container.appendChild(title);
  container.appendChild(description);
  container.appendChild(form);

  return container;
}
