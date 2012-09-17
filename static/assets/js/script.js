submitHandler = function (e) {
  window.location = '/' + document.getElementById('searchInput').value;
  e.preventDefault();
};

document.getElementById('searchForm').addEventListener("submit", submitHandler);