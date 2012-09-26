hasDatalist = function () {
  return 'options' in document.createElement('datalist');
};

submitHandler = function (e) {
  window.location = '/' + document.getElementById('searchInput').value;
  e.preventDefault();
};

document.getElementById('searchForm').addEventListener("submit", submitHandler);

if (!hasDatalist()) {
  content = 'Refer to the <a href="/projects">list of monitored projects</a> for a the project names.';
  document.getElementById('searchTip').innerHTML = content;
}
