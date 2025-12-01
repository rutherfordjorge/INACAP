export function createRefreshButton({ onRefresh }) {
  const button = document.createElement('button');
  button.className = 'action-button refresh-button';
  button.type = 'button';
  button.textContent = 'Recargar';
  button.addEventListener('click', () => onRefresh?.());
  return button;
}
