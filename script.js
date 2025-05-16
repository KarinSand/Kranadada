document.addEventListener("DOMContentLoaded", () => {
  let events = [];
  let deck = [];
  let placed = [];
  let score = 0;
  let incorrectStreak = 0;

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
      console.log("Kort laddade:", events.length);
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
      title: currentCard.dataset.title,
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
    incorrectStreak = 0;

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
    currentCard.className = "card";
    currentCard.setAttribute("draggable", "true");
    currentCard.dataset.year = ev.year;
    currentCard.dataset.title = ev.title;
    currentCard.innerHTML = `<div class="card-title">${ev.title}</div>`;
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
      incorrectStreak = 0;

      currentCard.innerHTML = `<div class="card-title">${currentCard.dataset.title}</div>`;

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
      incorrectStreak += 1;
      currentCard.classList.add("incorrect");
      setTimeout(() => currentCard.classList.remove("incorrect"), 1000);

      if (incorrectStreak >= 2) {
        fetch(`/hint/${encodeURIComponent(currentCard.dataset.title)}`)
          .then(res => res.json())
          .then(data => {
            currentCard.innerHTML = `
              <div class="card-title">${currentCard.dataset.title}</div>
              <div class="card-hint">${data.hint}</div>
            `;
          });
        incorrectStreak = 0;
      }
    }
  }

  function refreshDropzones() {
    timeline.querySelectorAll(".dropzone").forEach(z => z.remove());
    for (let i = 0; i <= placed.length; i++) {
      addDropzone(i);
    }
  }
});
