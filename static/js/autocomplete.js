document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("code");
  const dataList = document.getElementById("codeList");

  fetch("/static/data/autocomplete.json")
    .then(response => response.json())
    .then(data => {
      data.forEach(item => {
        const option = document.createElement("option");
        option.value = item;  // ここが重要
        dataList.appendChild(option);
      });
    });
});
