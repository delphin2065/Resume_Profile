let myBtn = document.querySelector("#downloadButton");
let myTable = document.querySelector("table");

myBtn.addEventListener("click", () => {
  const csv = tableToCSV(myTable);
  downloadCSV(csv, "table_data.csv");
});

function tableToCSV(myTable) {
  const rows = myTable.querySelectorAll("tr");
  return Array.from(rows, (row) => {
    const columns = row.querySelectorAll("th, td");
    return Array.from(columns, (column) => column.innerText).join(",");
  }).join("\n");
}

function downloadCSV(csv, filename) {
  const csvFile = new Blob([csv], { type: "text/csv" });
  const downloadLink = document.createElement("a");
  downloadLink.download = filename;
  downloadLink.href = URL.createObjectURL(csvFile);
  downloadLink.click();
}
