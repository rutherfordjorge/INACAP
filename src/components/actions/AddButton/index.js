export function createAddButton({ onAdd }) {
  const button = document.createElement('button');
  button.className = 'action-button add-button';
  button.type = 'button';
  button.textContent = 'Agregar';
  button.addEventListener('click', () => onAdd?.());
  return button;
}
