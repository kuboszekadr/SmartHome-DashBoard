var chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(231,233,237)'
};

// One common x-axis for values
var labels = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23'];

// Sensor values data
var values = {
    1: {1: [21.42,21.39,21.37,21.32,21.27,21.21,21.15,21.1,21.07,21.07,21.08,21.11,21.13,21.16,21.19,21.23,21.26,21.31,21.33,21.37,21.38,21.38,21.38,21.36],
        4: [22.22,22.1,21.97,21.9,21.83,21.79,21.79,21.8,21.83,21.85,21.9,21.95,22.03,22.13,22.2,22.3,22.37,22.4,22.53,22.6,22.55,22.51,22.35,22.22,22.03]},
    2: {2: [15.42,15.42,15.42,15.42,15.43,15.43,15.43,15.44,15.44,15.44,15.43,15.43,15.43,15.43,15.42,15.43,15.43,15.43,15.43,15.43,15.43,15.43,15.43,15.43,15.44]},
    3: {3: [2.02,2.02,2.02,2.02,2.02,2.02,2.02,2.02,2.02,2.02,2.02,2.02,2.03,2.03,2.03,2.03,2.03,2.03,2.02,2.02,2.02,2.02,2.02,2.02,2.02]},
    4: {4: [55.29,55.29,55.26,55.2,55.14,55.1,55.09,55.01,55.02,55.08,55.1,55.1,55.13,55.2,55.21,55.38,55.48,55.5,55.64,55.71,55.82,55.96,56.24,56.3,56.42]}
};

// Measures name dictionary
var measures = {
    1: 'Temperature',
    2: 'Water level',
    3: 'Ph',
    4: 'Humidity'
};

// Sensors dictionary
var sensors = {
    1: {'name': 'Water temperature', 'measures': [1]},
    2: {'name': 'Water level', 'measures': [2]},
    3: {'name': 'Ph', 'measures': [3]},
    4: {'name': 'Cover left', 'measures': [1, 4]},
    5: {'name': 'Cover center', 'measures': [1, 4]},
    6: {'name': 'Cover right', 'measures': [1, 4]}
};

var chartDatasets = [{}];

// Chart config
var chartConfig = {
    type: 'line',
    data: {
        labels: labels,
        datasets: chartDatasets
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: measures[1],
            fontColor: '#fff',
            fontSize: 16
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            x: {
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Month'
                }
            },
            y: {
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }
        },
        legend: {
            position: 'bottom'
        }
    }
};

var chart = new Chart(document.getElementById('canvas').getContext('2d'), chartConfig);
var measureForm = document.getElementById('measureSelect');
var sensorForm = document.getElementById('sensorSelectForm');

function udpateChart(measure, sensorIds)
{
    chartDatasets = [];
    var i = 0;

    // add cached sensor values into the chart
    for (const sensorId in sensorIds) {
        // get series color (ordered by sensorId)
        var clrKey = Object.keys(chartColors)[i];
        var clrValue = chartColors[clrKey];

        // create new chart dataset
        chartDataset = {
            label: sensors[sensorId]['name'], //series name
            backgroundColor: clrValue, // series color
            borderColor: clrValue,
            fill: false,
            data: values[measure][sensorId] // values to show
        };
        chartDatasets.push(chartDataset); // add series to the chart data
        i++;
    };

    // Update the chart
    chart.options.title.text = measures[measure];
    chart.data.datasets = chartDatasets;
    chart.update();
};

// measure click handlers
function onMeasureClick(measure) {
    var sensorIds = values[measure];
    udpateChart(measure, sensorIds);    
    
    // Check if additional sensor selector can be shown
    var sensorSelector = document.getElementById('sensorSelect');
    sensorSelector.style.display="none";
    
    if (Object.keys(sensorIds).length>1) {
        sensorSelector.style.display="block"; 
        fillSensorSelectForm(values[measure]);
    }
};

function fillSensorSelectForm(sensorIds) {
    sensorForm.options.length = 0;

    for (const sensorId in sensorIds) {
        var option = document.createElement('option');
        
        option.value = sensorId;
        option.text = sensors[sensorId]['name'];

        sensorForm.add(option);
    }
};

measureForm.addEventListener('change', 
    function() { onMeasureClick(measureForm.options[measureForm.selectedIndex].value); }
);

sensorForm.addEventListener('change', function() {
    sensorIds=[];
    for (let i = 0; i < sensorForm.options.length; i++) {
        const opt = sensorForm.options[i];
        opt.selected ? sensorIds[opt.value] = '' : {};
    };

    var measure = measureForm.value;
    udpateChart(measure, sensorIds);
});

document.onreadystatechange = function() {
    if (document.readyState != 'complete') {
        document.getElementById('canvas').style.display = "none";
        return;
    }
    document.getElementById('canvas').style.display = "block";
    onMeasureClick(1);
}