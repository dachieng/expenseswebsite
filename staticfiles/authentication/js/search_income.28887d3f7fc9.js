const searchField = document.getElementById("search_input");
const tableOutput = document.querySelector(".table-output");
const tableData = document.querySelector(".data-table");
const pagination = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
const noResult = document.querySelector(".no-results");

tableOutput.style.display = "none";
noResult.style.display = "none";

searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;
    pagination.style.display = "none"
    tbody.innerHTML = ""

    if (searchValue.trim().length > 0) {
        console.log(searchValue);
        fetch("/incomes/search-income/", {
                body: JSON.stringify({ searchText: searchValue }),
                method: "POST",
            })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                tableData.style.display = "none"
                tableOutput.style.display = "block";

                if (data.length === 0) {
                    tableOutput.style.display = "none";
                    noResult.style.display = "block";
                } else {
                    noResult.style.display = "none";
                    data.forEach((item) => {
                        tbody.innerHTML += `
                        <tr>
                        <td>${item.id}</td>
                        <td>${item.amount}</td>
                        <td>${item.source}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        </tr>`;
                    });
                }

            });
    } else {
        tableData.style.display = "block"
        pagination.style.display = "block"
        tableOutput.style.display = "none";

    }
})