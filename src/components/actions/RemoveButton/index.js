export function createRemoveButton({ onRemove }) {
  const button = document.createElement('button');
  button.className = 'action-button remove-button';
  button.type = 'button';
  button.textContent = 'Quitar';
  button.addEventListener('click', () => onRemove?.());
  return button;
}
