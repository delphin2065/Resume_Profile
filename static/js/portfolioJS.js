let add = document.querySelector("#add");
add.addEventListener("click", () => {
  let form = document.querySelector("form");

  let stockIDLabel = document.createElement("label");
  stockIDLabel.setAttribute("for", "stockID");
  stockIDLabel.setAttribute("class", "mt-1");
  stockIDLabel.setAttribute("id", "stockID");
  stockIDLabel.textContent = "股票代號";

  let stockIDInput = document.createElement("input");
  stockIDInput.setAttribute("type", "text");
  stockIDInput.setAttribute("id", "stockID");
  stockIDInput.setAttribute("name", "stockID");
  stockIDInput.setAttribute("class", "mt-1 ms-1");
  stockIDInput.setAttribute("required", "true");

  let stockWeightLabel = document.createElement("label");
  stockWeightLabel.setAttribute("for", "stockWeight");
  stockWeightLabel.setAttribute("class", "mt-1 ms-1");
  stockWeightLabel.setAttribute("id", "stockWeight");

  stockWeightLabel.textContent = "股票權重";

  let stockWeightInput = document.createElement("input");
  stockWeightInput.setAttribute("type", "number");
  stockWeightInput.setAttribute("id", "stockWeight");
  stockWeightInput.setAttribute("name", "stockWeight");
  stockWeightInput.setAttribute("class", "mt-1 ms-1");
  stockWeightInput.setAttribute("required", "true");
  stockWeightInput.setAttribute("step", "0.1");
  stockWeightInput.setAttribute("min", "0.0");
  stockWeightInput.setAttribute("max", "1.0");

  let brN = document.createElement("br");
  brN.setAttribute("id", "brN");

  form.appendChild(stockIDLabel);
  form.appendChild(stockIDInput);
  form.appendChild(stockWeightLabel);
  form.appendChild(stockWeightInput);
  form.appendChild(brN);
});

let minus = document.querySelector("#minus");
minus.addEventListener("click", () => {
  let form = document.querySelector("form");
  let stockIDLabel = document.querySelector("label#stockID");
  let stockIDInput = document.querySelector("input#stockID");
  let stockWeightLabel = document.querySelector("label#stockWeight");
  let stockWeightInput = document.querySelector("input#stockWeight");

  let brN = document.querySelector("br#brN");

  form.removeChild(brN);
  form.removeChild(stockIDLabel);
  form.removeChild(stockIDInput);
  form.removeChild(stockWeightLabel);
  form.removeChild(stockWeightInput);
});

let deleteTable = document.querySelector("#deleteTable");
deleteTable.addEventListener("click", () => {
  let divTableData = document.querySelector(".tableData");
  let tableDataframe = document.querySelector(".dataframe");
  if (tableDataframe) {
    tableDataframe.remove();
    if (mainFrame) {
      Plotly.purge(mainFrame);
    }
  }
});

document.addEventListener("DOMContentLoaded", () => {
  let dataframe = document.querySelector(".dataframe");
  if (dataframe) {
    let mainFrame = document.querySelector("#mainFrame");
    let data = [
      {
        x: list_date,
        y: list_net,
        type: "line",
        yaxis: "y",
        name: "portfolio cumPL",
      },
      {
        x: list_date,
        y: list_dd,
        fill: "tozeroy",
        yaxis: "y2",
        name: "max drow down",
      },
    ];
    let layout = {
      title: {
        text: "",
        font: { size: 24 },
        x: 0.5,
      },
      xaxis: {
        title: { text: "Date", font: { size: 10 } },
      },
      yaxis: {
        title: { text: "", font: { size: 10 } },
      },
      yaxis2: { title: "", overlaying: "y", side: "right" },
      legend: { x: 0.4, y: 1.1, orientation: "h" },
      margin: { t: 1 },
    };
    Plotly.newPlot(mainFrame, data, layout);
  }
});

window.addEventListener("resize", () => {
  mainFrame = document.querySelector("#mainFrame");
  Plotly.relayout(mainFrame, {
    width: window.innerWidth * 0.8, // 設定新的寬度
    height: window.innerHeight * 0.6, // 設定新的高度
  });
});
