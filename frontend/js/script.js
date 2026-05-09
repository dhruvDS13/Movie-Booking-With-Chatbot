const apiBase = window.location.origin.includes("8000") ? "" : "http://localhost:8000";
const userId = localStorage.getItem("bookmymovie_user") || crypto.randomUUID();
localStorage.setItem("bookmymovie_user", userId);

const chatLog = document.querySelector("#chatLog");
const chatForm = document.querySelector("#chatForm");
const chatInput = document.querySelector("#chatInput");
const movieGrid = document.querySelector("#movieGrid");
const showPanel = document.querySelector("#showPanel");
const movieSearch = document.querySelector("#movieSearch");

function addChat(role, text) {
  const bubble = document.createElement("div");
  bubble.className =
    role === "user"
      ? "ml-auto max-w-[85%] rounded-lg bg-emerald-500 px-3 py-2 text-sm text-zinc-950"
      : "max-w-[85%] whitespace-pre-line rounded-lg bg-zinc-800 px-3 py-2 text-sm text-zinc-100";
  bubble.textContent = text;
  chatLog.appendChild(bubble);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function getJson(path, options) {
  const response = await fetch(`${apiBase}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}

async function loadMovies(query = "") {
  const params = new URLSearchParams({ limit: "12" });
  if (query) params.set("q", query);
  const movies = await getJson(`/movies?${params.toString()}`);
  movieGrid.innerHTML = "";
  movies.forEach((movie) => {
    const card = document.createElement("article");
    card.className = "rounded-lg border border-zinc-800 bg-zinc-900 p-4";
    card.innerHTML = `
      <div class="flex items-start justify-between gap-3">
        <h3 class="font-semibold">${movie.title}</h3>
        <span class="rounded bg-zinc-800 px-2 py-1 text-xs">${movie.rating.toFixed(1)}</span>
      </div>
      <p class="mt-2 line-clamp-3 text-sm text-zinc-400">${movie.overview || "No overview available."}</p>
      <p class="mt-3 text-xs text-zinc-500">${movie.genres.slice(0, 3).join(" / ")}</p>
      <button class="mt-4 w-full rounded-md bg-zinc-100 px-3 py-2 text-sm font-semibold text-zinc-950">View Shows</button>
    `;
    card.querySelector("button").addEventListener("click", () => loadShows(movie));
    movieGrid.appendChild(card);
  });
}

async function loadShows(movie) {
  const shows = await getJson(`/shows?movie_id=${movie.id}`);
  showPanel.classList.remove("hidden");
  showPanel.innerHTML = `<h3 class="text-lg font-semibold">${movie.title} Shows</h3><div class="mt-3 grid gap-2"></div>`;
  const list = showPanel.querySelector("div");
  shows.slice(0, 10).forEach((show) => {
    const item = document.createElement("div");
    item.className = "flex flex-wrap items-center justify-between gap-3 rounded-md border border-zinc-800 p-3";
    item.innerHTML = `
      <div>
        <p class="font-medium">${show.theatre_name}</p>
        <p class="text-sm text-zinc-400">${show.city} | ${show.date} | ${show.time} | Rs ${show.price}</p>
      </div>
      <button class="rounded-md bg-emerald-500 px-3 py-2 text-sm font-semibold text-zinc-950">Seats</button>
    `;
    item.querySelector("button").addEventListener("click", () => loadSeats(show));
    list.appendChild(item);
  });
  showPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadSeats(show) {
  const data = await getJson(`/shows/${show.id}/seats`);
  const selected = new Set();
  showPanel.innerHTML = `
    <h3 class="text-lg font-semibold">${show.movie_title}</h3>
    <p class="text-sm text-zinc-400">${show.theatre_name} | ${show.date} | ${show.time}</p>
    <div id="seatGrid" class="mt-4 grid grid-cols-10 gap-2"></div>
    <button id="bookBtn" class="mt-4 rounded-md bg-emerald-500 px-4 py-2 text-sm font-semibold text-zinc-950">Book selected</button>
  `;
  const grid = document.querySelector("#seatGrid");
  [...data.booked, ...data.available].sort().forEach((seat) => {
    const button = document.createElement("button");
    const booked = data.booked.includes(seat);
    button.textContent = seat;
    button.disabled = booked;
    button.className = booked
      ? "h-9 rounded bg-zinc-800 text-xs text-zinc-600"
      : "h-9 rounded bg-zinc-100 text-xs font-semibold text-zinc-950";
    button.addEventListener("click", () => {
      if (selected.has(seat)) selected.delete(seat);
      else selected.add(seat);
      button.classList.toggle("bg-emerald-500");
      button.classList.toggle("bg-zinc-100");
    });
    grid.appendChild(button);
  });

  document.querySelector("#bookBtn").addEventListener("click", async () => {
    if (!selected.size) return alert("Please select seats.");
    const booking = await getJson("/bookings", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, show_id: show.id, seat_numbers: [...selected] }),
    });
    alert(`Booking confirmed: ${booking.booking_id} | Rs ${booking.total_amount}`);
    loadSeats(show);
  });
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;
  chatInput.value = "";
  addChat("user", message);
  addChat("assistant", "Typing...");
  const pending = chatLog.lastElementChild;
  try {
    const data = await getJson("/chat", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, message }),
    });
    pending.textContent = data.reply;
  } catch (error) {
    pending.textContent = error.message;
  }
});

document.querySelector("#searchBtn").addEventListener("click", () => loadMovies(movieSearch.value.trim()));
movieSearch.addEventListener("keydown", (event) => {
  if (event.key === "Enter") loadMovies(movieSearch.value.trim());
});

addChat("assistant", "Hi! Would you like a movie recommendation or should we start a booking?");
loadMovies();
