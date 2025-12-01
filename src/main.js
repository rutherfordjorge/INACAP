import { defaultItems } from './data/items.js';
import { restoreSession, signOut } from './services/auth/office365Auth.js';
import { createLoginView } from './views/login/loginView.js';
import { createListingView } from './views/listing/listingView.js';

const appContainer = document.querySelector('#app');
let currentUser = restoreSession();
let items = [...defaultItems];

function render(view) {
  appContainer.innerHTML = '';
  appContainer.appendChild(view);
}

function refreshListing() {
  render(
    createListingView({
      items,
      user: currentUser,
      onAdd: handleAdd,
      onRemove: handleRemove,
      onRefresh: handleRefresh,
      onSignOut: handleSignOut,
    })
  );
}

function handleAdd() {
  const nextId = items.length ? Math.max(...items.map((item) => item.id)) + 1 : 1;
  items = [
    ...items,
    { id: nextId, name: `Elemento nuevo #${nextId}`, owner: currentUser.displayName },
  ];
  refreshListing();
}

function handleRemove() {
  items = items.slice(0, -1);
  refreshListing();
}

function handleRefresh() {
  items = [...defaultItems];
  refreshListing();
}

function handleSignOut() {
  signOut();
  currentUser = null;
  showLogin();
}

function showLogin() {
  render(
    createLoginView({
      onSuccess: (session) => {
        currentUser = session;
        refreshListing();
      },
    })
  );
}

if (currentUser) {
  refreshListing();
} else {
  showLogin();
}
