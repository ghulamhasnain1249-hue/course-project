const bookingForm = document.getElementById("booking-form");
const dateField = document.getElementById("reservation_date");
const slotSelect = document.getElementById("reservation_slot");
const messageBox = document.getElementById("booking-message");
const reservationsBody = document.getElementById("reservations-body");

const SLOTS = {
  1: "10:00", 2: "11:00", 3: "12:00", 4: "13:00",
  5: "14:00", 6: "15:00", 7: "16:00", 8: "17:00",
  9: "18:00", 10: "19:00", 11: "20:00", 12: "21:00",
};

function todayISO() {
  const date = new Date();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${date.getFullYear()}-${month}-${day}`;
}

function showMessage(text, isError = false) {
  if (!messageBox) return;
  messageBox.textContent = text;
  messageBox.className = isError ? "error" : "success";
}

function renderSlots(bookedSlots = []) {
  if (!slotSelect) return;
  slotSelect.replaceChildren();
  Object.entries(SLOTS).forEach(([value, label]) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = bookedSlots.includes(Number(value))
      ? `${label} (booked)`
      : label;
    option.disabled = bookedSlots.includes(Number(value));
    slotSelect.appendChild(option);
  });
}

async function fetchBookingsForDate(date) {
  const response = await fetch(`/bookings?date=${encodeURIComponent(date)}`);
  if (!response.ok) return [];
  const data = await response.json();
  return Array.isArray(data) ? data : [];
}

async function refreshFormForDate() {
  if (!dateField) return;
  const date = dateField.value || todayISO();
  dateField.value = date;

  try {
    const bookings = await fetchBookingsForDate(date);
    renderSlots(bookings.map((booking) => booking.reservation_slot));
    showMessage(bookings.length
      ? `${bookings.length} booking(s) already on this date.`
      : "No bookings for this date yet.");
  } catch {
    renderSlots();
    showMessage("Could not load availability. Please try again.", true);
  }
}

async function loadReservationsTable() {
  if (!reservationsBody) return;
  try {
    const response = await fetch("/bookings/all");
    const data = await response.json();
    reservationsBody.replaceChildren();

    if (!response.ok || !Array.isArray(data) || data.length === 0) {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 4;
      cell.textContent = "No Booking found";
      row.appendChild(cell);
      reservationsBody.appendChild(row);
      return;
    }

    data.forEach((booking) => {
      const row = document.createElement("tr");
      [
        booking.first_name,
        booking.reservation_date,
        booking.slot_time || booking.reservation_slot,
        booking.id,
      ].forEach((value) => {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
      });
      reservationsBody.appendChild(row);
    });
  } catch {
    showMessage("Could not load reservations.", true);
  }
}

async function submitBooking(event) {
  event.preventDefault();
  const firstName = document.getElementById("first_name").value.trim();
  const csrfToken = bookingForm.querySelector("[name=csrfmiddlewaretoken]").value;

  if (!firstName) {
    showMessage("First name is required.", true);
    return;
  }

  try {
    const response = await fetch("/bookings/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        first_name: firstName,
        reservation_date: dateField.value,
        reservation_slot: slotSelect.value,
      }),
    });

    if (response.status === 201) {
      showMessage("Booking confirmed!");
      bookingForm.reset();
      dateField.value = todayISO();
      await refreshFormForDate();
    } else if (response.status === 409) {
      showMessage("That slot is already booked. Pick another.", true);
      await refreshFormForDate();
    } else {
      const body = await response.json().catch(() => ({}));
      showMessage(body.error || "Something went wrong.", true);
    }
  } catch {
    showMessage("Could not submit the booking. Please try again.", true);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (dateField) {
    dateField.value = todayISO();
    dateField.min = todayISO();
    dateField.addEventListener("change", refreshFormForDate);
    refreshFormForDate();
  }
  if (bookingForm) bookingForm.addEventListener("submit", submitBooking);
  if (reservationsBody) loadReservationsTable();
});