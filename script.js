// Enkel drag & drop-funktionalitet
let draggedCard = null;

// Samla alla kort
const cards = document.querySelectorAll('.card');
const timeline = document.getElementById('timeline');
const deck = document.getElementById('deck');

cards.forEach(card => {
  card.addEventListener('dragstart', () => {
    draggedCard = card;
    card.classList.add('dragging');
  });

  card.addEventListener('dragend', () => {
    draggedCard = null;
    card.classList.remove('dragging');
  });
});

// Tillåt drop på tidslinjen
timeline.addEventListener('dragover', (e) => {
  e.preventDefault();
});

timeline.addEventListener('drop', (e) => {
  e.preventDefault();
  if (draggedCard) {
    timeline.appendChild(draggedCard);
  }
});

// Tillåt drop i "deck" om man vill lägga tillbaka kortet
deck.addEventListener('dragover', (e) => {
  e.preventDefault();
});

deck.addEventListener('drop', (e) => {
  e.preventDefault();
  if (draggedCard) {
    deck.appendChild(draggedCard);
  }
});
