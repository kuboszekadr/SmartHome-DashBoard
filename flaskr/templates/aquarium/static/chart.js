var chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(231,233,237)'
};

var labels = {};  // One common x-axis for values
var values = {};  // Sensor values data

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

// var chart = new Chart(document.getElementById('canvas').getContext('2d'), chartConfig);
var chart; //to be initiliesed once data is in place
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
            pointRadius: 0,
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
        document.getElementById('pageContent').style.display = "none";
        return;
    }

    $.ajaxSetup({async: false});
    $.get(url='http://127.0.1:5001/api',
        function(data){
            values = data["readings"],
            labels = data["labels"]
            chartConfig.data.labels = labels;
        },
        dataType="json"
        )
    
    chart = new Chart(document.getElementById('canvas').getContext('2d'), chartConfig);

    document.getElementById('pageContent').style.display = "block";
    onMeasureClick(1);
}
