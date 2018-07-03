/*
    Javascript file. Generates the graphs with data from the database,
    taking out the income and expenditures, shows 2 graphs, circular and linear.
    Use Ajax to obtain the data from View.
*/

var endpoint = '/mycash/api/chart/data/'
var type_chart = 'line'

function typeChart(){
    list_type = document.chart.type_chart;
    options = list_type.options;
    num = list_type.selectedIndex
    type_chart = options[num].value;
    $.ajax({
        method: "GET",
        url: endpoint,
        success: function(data){
            income_label = data.income_label
            expense_label = data.expense_label
            income_data = data.income_amount
            expense_data = data.expense_amount
            setChart()

            console.log(type_chart)
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        }
    })
}

function setChart(){
    var ctx2 = document.getElementById("myChart2").getContext('2d');
    var ctx3 = document.getElementById("myChart3").getContext('2d');

    if (window.chart2 != undefined)
        window.chart2.destroy();

    window.chart2 = new Chart(ctx2, {
        type: type_chart,
        data: {
            labels: income_label,
            datasets: [{
                label: 'Incomes',
                data: income_data,
                backgroundColor: [
                'rgba(51, 255, 97, 0.5)',
                'rgba(51, 255, 97, 0.5)',
                'rgba(51, 255, 97, 0.5)',
                'rgba(51, 255, 97, 0.5)',
                'rgba(51, 255, 97, 0.5)',
                'rgba(51, 255, 97, 0.5)',
                'rgba(51, 255, 97, 0.5)',
                ],
                borderColor: [
                    'rgba(51, 255, 97, 1)',
                    'rgba(51, 255, 97, 1)',
                    'rgba(51, 255, 97, 1)',
                    'rgba(51, 255, 97, 1)',
                    'rgba(51, 255, 97, 1)',
                    'rgba(51, 255, 97, 1)',
                    'rgba(51, 255, 97, 1)',
                ],
                borderWidth: 1
            }]
        },

        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });

    if (window.chart3 != undefined)
        window.chart3.destroy();

    window.chart3 = new Chart(ctx3, {
        type: type_chart,
        data: {
            labels: expense_label,
            datasets: [{
                label: 'Expenses',
                data: expense_data,
                backgroundColor: [
                'rgba(231, 126, 207, 0.5)',
                'rgba(231, 126, 207, 0.5)',
                'rgba(231, 126, 207, 0.5)',
                'rgba(231, 126, 207, 0.5)',
                'rgba(231, 126, 207, 0.5)',
                'rgba(231, 126, 207, 0.5)',
                'rgba(231, 126, 207, 0.5)',
                ],
                borderColor: [
                    'rgba(231, 126, 207, 1)',
                    'rgba(231, 126, 207, 1)',
                    'rgba(231, 126, 207, 1)',
                    'rgba(231, 126, 207, 1)',
                    'rgba(231, 126, 207, 1)',
                    'rgba(231, 126, 207, 1)',
                    'rgba(231, 126, 207, 1)',
                ],
                borderWidth: 1
            }]
        },

        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}