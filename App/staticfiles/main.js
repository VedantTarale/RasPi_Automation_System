var temp_data = {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Temperature',
                data: [],
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
}

var pressure_data = {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Pressure',
                data: [],
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
}

var moisture_data = {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Moisture',
                data: [],
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
}

const ctx0 = document.getElementById('tempChart')
const ctx1 = document.getElementById('pressureChart')
const ctx2 = document.getElementById('moistureChart')

var temp_chart = new Chart(ctx0, temp_data)
var pressure_chart = new Chart(ctx1, pressure_data)
var moisture_chart = new Chart(ctx2, moisture_data)

const socket_url = 'ws://localhost:8000/ws/reading/'
var socket = new WebSocket(socket_url)
socket.onmessage = function (e) {
    var data = JSON.parse(e.data)
    console.log(data)
    temp_vals = data.map((entry) => entry.temp)
    pressure_vals = data.map((entry) => entry.pressure)
    moisture_vals = data.map((entry) => entry.moisture)
    time = data.map((entry) => {
        let dateObject = new Date(entry.time)

        let formattedTime = dateObject.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        })

        return formattedTime
    })
    temp_data.data.labels = time
    pressure_data.data.labels = time
    moisture_data.data.labels = time
    

    temp_data.data.datasets[0].data = temp_vals
    pressure_data.data.datasets[0].data = pressure_vals
    moisture_data.data.datasets[0].data = moisture_vals

    temp_chart.update()
    pressure_chart.update()
    moisture_chart.update()
}