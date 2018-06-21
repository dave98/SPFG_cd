/*
    Javascript file. Generates the graphs with data from the database,
    taking out the income and expenditures, shows 2 graphs, circular and linear.
    Use Ajax to obtain the data from View.
*/

var endpoint = '/mycash/api/chart/data/'
var defaultData = []
var labels = [];
var type_chart = 'bar'

$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        income_label = data.income_label
        expense_label = data.expense_label
        income_data = data.income_amount
        expense_data = data.expense_amount
        setChart()

        //console.log(data)
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setChart(){
    // var ctx = document.getElementById("myChart").getContext('2d');
    var ctx2 = document.getElementById("myChart2").getContext('2d');
    var ctx3 = document.getElementById("myChart3").getContext('2d');

    // Circular Chart on Income
    var myChart = new Chart(ctx2, {
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

    // Circular Chart on Expense
    var myChart = new Chart(ctx3, {
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

    // Lineal Chart on Income
    /*var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: income_label,
            datasets: [{
                label: 'Incomes',
                data: income_data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
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
    });*/
}