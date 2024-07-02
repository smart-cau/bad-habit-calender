const fullCalendar = () => {
  /**
   * Update the clicked day.
   * @param {dateString} ex) 2024-01-01
   * @return {void}
   */
  const updateCurrentDay = (dateString) => {
    const prevClickedDay = document.querySelector(".fc-clicked-day");
    if (prevClickedDay) {
      prevClickedDay.classList.remove("fc-clicked-day");
    }
    const clickeDay = document.querySelector(
      `td[data-date="${dateString}"] .fc-daygrid-day-top`
    );
    if (clickeDay) {
      clickeDay.classList.add("fc-clicked-day");
    }
  };

  const calendarEl = document.getElementById("calendar");
  const calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: {
      start: "prev",
      center: "title",
      end: "next",
    },
    titleFormat: {
      month: "short",
    },
    dayCellContent: function (info) {
      const number = document.createElement("button");
      number.classList.add("fc-daygrid-day-number");
      number.innerHTML = info.dayNumberText.replace("일", "");
      return {
        html: number.outerHTML,
      };
    },
    dateClick: ({ date, view }) => {
      sessionStorage.setItem("currentDay", date.toLocaleDateString("en-CA"));
      updateCurrentDay(date.toLocaleDateString("en-CA"));
      view.calendar.gotoDate(date);
    },
    locale: "ko",
    initialView: "dayGridMonth",
  });
  calendar.render();

  const currentDay = document.querySelector(
    ".fc-day-today .fc-daygrid-day-top"
  );
  if (currentDay) {
    currentDay.classList.add("fc-clicked-day");
  }

  document.querySelector(".fc-prev-button").addEventListener("click", () => {
    const currentDate = sessionStorage.getItem("currentDay");
    updateCurrentDay(currentDate);
  });
  document.querySelector(".fc-next-button").addEventListener("click", () => {
    const currentDate = sessionStorage.getItem("currentDay");
    updateCurrentDay(currentDate);
  });
};
