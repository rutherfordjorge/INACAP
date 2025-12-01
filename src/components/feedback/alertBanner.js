export function createAlertBanner({ type = 'info', message }) {
  const banner = document.createElement('div');
  banner.className = `alert-banner alert-${type}`;
  banner.textContent = message;
  return banner;
}
