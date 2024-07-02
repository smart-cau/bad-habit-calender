const tempData = [
  { title: "유튜브 1시간 이상 보기", success: false },
  { title: "개발 25시간 이상 하기", success: true },
];
const cElm = (elementType) => document.createElement(elementType);

const showCurrentDayHabbit = (data) => {
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
    div.textContent = item.title;
    li.appendChild(image);
    li.appendChild(div);
    ul.appendChild(li);
  });
  return ul;
};

const updateCurrentDayHabbit = (data) => {
  const elm = showCurrentDayHabbit(tempData);
  const currentDayHabbit = document.querySelector("#currentDayHabbit");
  currentDayHabbit.innerHTML = "";
  currentDayHabbit.appendChild(elm);
};

updateCurrentDayHabbit(tempData);
