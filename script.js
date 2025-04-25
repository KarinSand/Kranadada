// Öppna/stäng sidomeny
function openSidebar() {
  document.getElementById("sidebar").style.width = "250px";
}

function closeSidebar() {
  document.getElementById("sidebar").style.width = "0";
}

// Inloggning
function login() {
  const user = document.getElementById("username").value;
  if (user.trim() !== "") {
    alert(`Välkommen, ${user}!`);
    document.getElementById("logoutBtn").style.display = "inline-block";
  } else {
    alert("Fyll i ett användarnamn!");
  }
}

// Utloggning
function logout() {
  document.getElementById("username").value = "";
  alert("Du har loggats ut.");
  document.getElementById("logoutBtn").style.display = "none";
}

// Starta spel – skicka POST-förfrågan till /start_game
document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.getElementById('startGameBtn');
  if (startBtn) {
    startBtn.addEventListener('click', function () {
      console.log('Knappen har klickats!');

      fetch('/start_game', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Serverfel: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.log(data);
          updateTimeline(data.timeline);
        })
        .catch(error => {
          console.error('Fel vid förfrågan:', error);
        });
    });
  }
});

// Uppdatera tidslinjen visuellt
function updateTimeline(timeline) {
  const timelineDiv = document.getElementById('timeline');
  timelineDiv.innerHTML = ''; // Rensa

  timeline.forEach(card => {
    const cardElement = document.createElement('div');
    cardElement.className = 'timeline-card';
    cardElement.textContent = `${card.name} (${card.year})`;
    timelineDiv.appendChild(cardElement);
  });
}



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
