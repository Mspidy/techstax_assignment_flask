// this is only for frontend JS (fetch + refresh)
function fetchEvents() {
  fetch("/events")
    .then(res => res.json())
    .then(data => {
      const list = document.getElementById("event-list");
      list.innerHTML = "";
      data.forEach(event => {
        const li = document.createElement("li");
        li.textContent = event;
        list.appendChild(li);
      });
    });
}

// Load every 15 seconds
setInterval(fetchEvents, 15000);
fetchEvents();
