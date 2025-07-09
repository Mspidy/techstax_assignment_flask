// this is only for frontend JS (fetch + refresh)
// function fetchEvents() {
//   fetch("/events")
//     .then(res => res.json())
//     .then(data => {
//       const list = document.getElementById("event-list");
//       list.innerHTML = "";
//       data.forEach(event => {
//         const li = document.createElement("li");
//         li.textContent = event;
//         list.appendChild(li);
//       });
//     });
// }

// // Load every 15 seconds
// setInterval(fetchEvents, 15000);
// fetchEvents();

let countdown = 15;
const countdownElement = document.getElementById('countdown');

function fetchEvents() {
  fetch('/events')
    .then(res => res.json())
    .then(data => {
        console.log(data)
      const list = document.getElementById('event-list');
      list.innerHTML = "";
      data.forEach(event => {
        const el = formatEvent(event);
        list.appendChild(el);
      });
      showToast();
    });

  // Reset countdown
  countdown = 15;
}
function formatEvent(event) {
  const ts = new Date(event.timestamp);
  const formattedDate = ts.toLocaleString('en-GB', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
    timeZone: 'UTC'
  }) + ' UTC';

  const li = document.createElement('li');
  li.classList.add('event-item', event.event_type); // apply push / pull_request / merge class

  let content = '';

  if (event.event_type === 'push') {
    content = `
      <p><strong>${event.author}</strong> pushed to <strong>${event.to_branch}</strong></p>
      <p class="timestamp">${formattedDate}</p>
    `;
  } else if (event.event_type === 'pull_request') {
    content = `
      <p><strong>${event.author}</strong> submitted a pull request: <strong>${event.title || '-'}</strong></p>
      <p>from <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong></p>
      <p class="body">📝 ${event.body || '-'}</p>
      <p class="timestamp">${formattedDate}</p>
    `;
  } else if (event.event_type === 'merge') {
    content = `
      <p><strong>${event.author}</strong> merged <strong>${event.from_branch}</strong> to <strong>${event.to_branch}</strong></p>
      <p class="title">📌 ${event.title || '-'}</p>
      <p class="body">📝 ${event.body || '-'}</p>
      <p class="timestamp">${formattedDate}</p>
    `;
  }

  li.innerHTML = content;
  return li;  // ✅ returning a DOM Node now
}


// Update countdown every second
setInterval(() => {
  countdown--;
  if (countdownElement) {
    countdownElement.textContent = countdown;
  }

  if (countdown <= 0) {
    fetchEvents();
  }
}, 1000);

function showToast() {
  const toast = document.getElementById("toast");
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

document.getElementById("legend-toggle").addEventListener("click", () => {
  const legend = document.getElementById("legend-content");
  legend.style.display = legend.style.display === "block" ? "none" : "block";
});



// Initial load
fetchEvents();

