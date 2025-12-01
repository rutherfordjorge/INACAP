import { createAddButton } from '../../components/actions/AddButton/index.js';
import { createRemoveButton } from '../../components/actions/RemoveButton/index.js';
import { createRefreshButton } from '../../components/actions/RefreshButton/index.js';
import { createAlertBanner } from '../../components/feedback/alertBanner.js';

export function createListingView({ items, onAdd, onRemove, onRefresh, onSignOut, user }) {
  const container = document.createElement('section');
  container.className = 'card listing-view';

  const header = document.createElement('div');
  header.className = 'card-header';

  const title = document.createElement('h2');
  title.textContent = 'Listado principal';

  const userInfo = document.createElement('div');
  userInfo.className = 'user-info';
  userInfo.textContent = user?.displayName ?? 'Sesión activa';

  const signOutButton = document.createElement('button');
  signOutButton.className = 'link-button';
  signOutButton.type = 'button';
  signOutButton.textContent = 'Cerrar sesión';
  signOutButton.addEventListener('click', onSignOut);

  userInfo.appendChild(signOutButton);

  header.appendChild(title);
  header.appendChild(userInfo);

  const actionsWrapper = document.createElement('div');
  actionsWrapper.className = 'actions-wrapper';
  actionsWrapper.appendChild(createAddButton({ onAdd }));
  actionsWrapper.appendChild(createRemoveButton({ onRemove }));
  actionsWrapper.appendChild(createRefreshButton({ onRefresh }));

  const listContainer = document.createElement('ul');
  listContainer.className = 'item-list';
  listContainer.setAttribute('aria-label', 'Listado de elementos');

  if (!items.length) {
    listContainer.appendChild(
      createAlertBanner({
        type: 'info',
        message: 'No hay elementos disponibles en este momento.',
      })
    );
  } else {
    items.forEach((item) => {
      const listItem = document.createElement('li');
      listItem.className = 'item-row';

      const name = document.createElement('span');
      name.className = 'item-name';
      name.textContent = item.name;

      const owner = document.createElement('span');
      owner.className = 'item-owner';
      owner.textContent = item.owner;

      listItem.appendChild(name);
      listItem.appendChild(owner);
      listContainer.appendChild(listItem);
    });
  }

  container.appendChild(header);
  container.appendChild(actionsWrapper);
  container.appendChild(listContainer);

  return container;
}
