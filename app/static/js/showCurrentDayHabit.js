const cElm = (elementType) => document.createElement(elementType);

const showCurrentDayhabit = (data) => {
  const ul = cElm("ul");
  ul.className = "overflow-y-auto h-[calc(100vh-35rem)] w-full space-y-4";
  data.forEach((item) => {
    const li = cElm("li");
    li.className = "flex items-center gap-4 p-4 bg-gray-100 rounded-md";
    const image = cElm("img");
    image.src = item.success
      ? "/static/images/success.png"
      : "/static/images/fail.png";
    const div = cElm("div");
    div.textContent = item.content;
    li.appendChild(image);
    li.appendChild(div);
    ul.appendChild(li);
  });
  return ul;
};

const updateCurrentDayhabit = (data) => {
  const elm = showCurrentDayhabit(data);
  const currentDayhabit = document.querySelector("#currentDayhabit");
  currentDayhabit.innerHTML = "";
  currentDayhabit.appendChild(elm);
};

const queryParam = new URLSearchParams(window.location.search);
const currentDate =
  queryParam.get("currentDay") || new Date().toLocaleDateString("en-CA");
fetch(`/api/enrolls?currentDay=${currentDate}`)
  .then((response) => response.json())
  .then((data) => {
    updateCurrentDayhabit(data);
  });
