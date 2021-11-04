const renderChart = (labels, data) => {
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            //labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            labels: labels,

            datasets: [{
                label: 'Last 7 days',
                //data: [12, 19, 3, 5, 2, 3],
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Expenses Per Category'
            }
        }
    });
}

// make an api call to fetch the data

getChartData = () => {
    fetch("/income-summary/").then(res => res.json()).then(results => {
        console.log(results);

        const category_data = results.income_source_data

        const [labels, data] = [Object.keys(category_data), Object.values(category_data)]



        renderChart(labels, data)
    })
}

document.onload = getChartData()