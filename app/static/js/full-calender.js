const fullCalendar = () => {
  /**
   * Update the clicked day.
   * @param {dateString} ex) 2024-01-01
   * @return {void}
   */
  const updateCurrentDay = (dateString) => {
    const clickeDay = document.querySelector(
      `td[data-date="${dateString}"] .fc-daygrid-day-top`
    );
    if (clickeDay) {
      clickeDay.classList.add("fc-clicked-day");
    }
  };

  const queryParam = new URLSearchParams(window.location.search);
  const currentDate =
    queryParam.get("currentDay") || new Date().toLocaleDateString("en-CA");

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
    initialDate: currentDate,
    dayCellContent: function (info) {
      const number = document.createElement("button");
      number.classList.add("fc-daygrid-day-number");
      number.innerHTML = info.dayNumberText.replace("일", "");
      return {
        html: number.outerHTML,
      };
    },
    dateClick: ({ date }) => {
      window.location.href = `?currentDay=${date.toLocaleDateString("en-CA")}`;
    },
    locale: "ko",
    initialView: "dayGridMonth",
  });
  calendar.render();

  updateCurrentDay(currentDate);

  document.querySelector(".fc-prev-button").addEventListener("click", () => {
    updateCurrentDay(currentDate);
  });
  document.querySelector(".fc-next-button").addEventListener("click", () => {
    updateCurrentDay(currentDate);
  });
};
