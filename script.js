let events = [];
let deck = [];
let placed = [];
let score = 0;

const startBtn = document.getElementById("start-btn");
const gameScreen = document.getElementById("game-screen");
const startScreen = document.getElementById("start-screen");
const timeline = document.getElementById("timeline");
const currentCard = document.getElementById("current-card");
const scoreEl = document.getElementById("score");

fetch("/events")
  .then((res) => res.json())
  .then((data) => {
    events = data;
  });

startBtn.addEventListener("click", () => {
  if (events.length === 0) {
    alert("Kort laddas, försök igen strax.");
    return;
  }
  startGame();
});

currentCard.addEventListener("dragstart", (e) => {
  e.dataTransfer.setData("text/plain", JSON.stringify({
    title: currentCard.textContent,
    year: currentCard.dataset.year
  }));
  currentCard.classList.add("dragging");
});

currentCard.addEventListener("dragend", () => currentCard.classList.remove("dragging"));

function startGame() {
  score = 0;
  scoreEl.textContent = score;
  placed = [];
  deck = shuffle([...events]);

  timeline.innerHTML = "";

  startScreen.classList.add("hidden");
  gameScreen.classList.remove("hidden");

  const firstCard = deck.pop();
  const firstCardElement = document.createElement("div");
  firstCardElement.className = "card correct";
  firstCardElement.textContent = `${firstCard.title} (${firstCard.year})`;
  timeline.appendChild(firstCardElement);

  placed.push({ title: firstCard.title, year: firstCard.year });

  refreshDropzones();
  drawNextCard();
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function drawNextCard() {
  if (deck.length === 0) {
    currentCard.textContent = "Spelet slut!";
    currentCard.dataset.year = "";
    currentCard.setAttribute("draggable", "false");
    currentCard.classList.add("finished");
    return;
  }

  const ev = deck.pop();
  currentCard.textContent = ev.title;
  currentCard.dataset.year = ev.year;
  currentCard.className = "card";
  currentCard.setAttribute("draggable", "true");
}

function addDropzone(position) {
  const dz = document.createElement("div");
  dz.className = "dropzone";
  dz.dataset.index = position;
  dz.addEventListener("dragover", (e) => { e.preventDefault(); dz.classList.add("highlight"); });
  dz.addEventListener("dragleave", () => dz.classList.remove("highlight"));
  dz.addEventListener("drop", handleDrop);

  const cards = timeline.querySelectorAll(".card");
  const referenceNode = cards[position] || null;
  timeline.insertBefore(dz, referenceNode);
}

function handleDrop(e) {
  e.preventDefault();
  this.classList.remove("highlight");

  const { title, year } = JSON.parse(e.dataTransfer.getData("text/plain"));
  const idx = parseInt(this.dataset.index, 10);
  const yr = parseInt(year, 10);

  const prev = placed[idx - 1];
  const next = placed[idx];
  const ok = (!prev || prev.year <= yr) && (!next || yr <= next.year);

  if (ok) {
    score += 1;
    scoreEl.textContent = score;

    const newCard = document.createElement("div");
    newCard.className = "card correct";
    newCard.textContent = `${title} (${year})`;

    timeline.insertBefore(newCard, this);
    placed.splice(idx, 0, { title, year: yr });

    refreshDropzones();
    drawNextCard();
  } else {
    score = Math.max(0, score - 1);
    scoreEl.textContent = score;
    currentCard.classList.add("incorrect");
    setTimeout(() => currentCard.classList.remove("incorrect"), 1000);
  }  
}

function refreshDropzones() {
  timeline.querySelectorAll(".dropzone").forEach(z => z.remove());

  for (let i = 0; i <= placed.length; i++) {
    addDropzone(i);
  }
}
