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
      const list = document.getElementById('event-list');
      list.innerHTML = "";
      data.forEach(event => {
        const li = document.createElement('li');
        li.textContent = event;
        list.appendChild(li);
      });
      showToast();
    });

  // Reset countdown
  countdown = 15;
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


// Initial load
fetchEvents();

