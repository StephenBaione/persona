function format_track_analysis_values(analysis_values) {
    let track_cards = document.getElementsByClassName("track-card-back");
    for(let i = 0; i < analysis_values.length; i++) {
        let value = analysis_values[i];
        var danceability = (value["danceability"] * 100).toFixed(0);
        var energy = (value["energy"] * 100).toFixed(0);
        var key = value["key"];
        var loudness = (Math.abs((value["loudness"] / 60)) * 100).toFixed(0);
        var acousticness = (value["acousticness"] * 100).toFixed(0);
        var liveness = (value["liveness"] * 100).toFixed(0);
        var tempo = value["tempo"].toFixed(0);
        var analysis_tags = track_cards[i].getElementsByTagName('p');
        analysis_tags[0].innerText = danceability + "%";
        analysis_tags[1].innerText = energy + "%";
        analysis_tags[2].innerText = key;
        analysis_tags[3].innerText = loudness + "%";
        analysis_tags[4].innerText = acousticness + "%";
        analysis_tags[5].innerText = liveness + "%";
        analysis_tags[6].innerText = tempo;
    }
}

function populate_top_tracks_average_chart(top_tracks_average) {
    var ctx = document.getElementById('top_tracks_average').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Danceability', 'Energy', 'Loudness', 'Acousticness', 'Liveness'],
            datasets: [{
                data: [
                    top_tracks_average["danceability"],
                    top_tracks_average["energy"],
                    top_tracks_average["loudness"],
                    top_tracks_average["acousticness"],
                    top_tracks_average["liveness"]
                ],
                backgroundColor: [
                    '#983EFA',
                    'yellow',
                    'red',
                    'cyan',
                    'pink'
                ],
                borderColor: [
                    ''
                ],
                borderWidth: 1
            }],
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5,
                        max: 100
                    }
                }]
            },
            legend: {
                display: true,
                position: 'bottom',
                fillcolor: "yellow",
                labels: {
                    fontColor: "white",
                    fontStyle: "bold"
                },
                onHover: function (e) {
                    e.target.style.cursor = 'pointer'
                },
                onLeave: function (e) {
                    e.target.style.cursor = 'auto'
                }
            },
            title: {
                display: true,
                fontSize: '25',
                fontColor: 'white',
                text: 'Average For Top Songs'
            }
        }
    });
}

function populate_danceability_chart(audio_analysis, top_tracks) {
    let danceability = [];
    let labels = [];
    console.log(top_tracks);
    for(var i = 0; i < audio_analysis.length; i++) {
        console.log(audio_analysis[i]["danceability"]);
        danceability.push((audio_analysis[i]['danceability'] * 100).toFixed(0));
        labels.push(top_tracks[i]["name"]);
    }
    console.log(danceability);
    var ctx = document.getElementById('danceability-of-top-tracks').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: danceability,
                backgroundColor: '#983EFA',
                borderColor: [
                    ''
                ],
                borderWidth: 1
            }],
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5,
                        max: 100
                    }
                }]
            },
            title: {
                display: true,
                fontSize: '25',
                fontColor: 'white',
                text: 'Danceability of Top Tracks'
            }
        }
    });
}

function populate_energy_chart(audio_analysis, top_tracks) {
    let energy = [];
    let labels = [];
    for(var i = 0; i < audio_analysis.length; i++) {
        energy.push((audio_analysis[i]['energy'] * 100).toFixed(0));
        labels.push(top_tracks[i]["name"]);
    }
    var ctx = document.getElementById('energy-of-top-tracks').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: energy,
                backgroundColor: 'yellow',
                borderColor: [
                    ''
                ],
                borderWidth: 1
            }],
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5,
                        max: 100
                    }
                }]
            },
            title: {
                display: true,
                fontSize: '25',
                fontColor: 'white',
                text: 'Energy of Top Tracks'
            }
        }
    });
}

function populate_loudness_chart(audio_analysis, top_tracks) {
    let loudness = [];
    let labels = [];
    for(var i = 0; i < audio_analysis.length; i++) {
        loudness.push(Math.abs(audio_analysis[i]['loudness'] / 60 * 100).toFixed(0));
        labels.push(top_tracks[i]["name"]);
    }
    var ctx = document.getElementById('loudness-of-top-tracks').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: loudness,
                backgroundColor: 'red',
                borderColor: [
                    ''
                ],
                borderWidth: 1
            }],
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5,
                        max: 100
                    }
                }]
            },
            title: {
                display: true,
                fontSize: '25',
                fontColor: 'white',
                text: 'Loudness of Top Tracks'
            }
        }
    });
}

function populate_acousticness_chart(audio_analysis, top_tracks) {
    let acousticness = [];
    let labels = [];
    for(var i = 0; i < audio_analysis.length; i++) {
        acousticness.push((audio_analysis[i]['acousticness'] * 100).toFixed(0));
        labels.push(top_tracks[i]["name"]);
    }
    var ctx = document.getElementById('acousticness-of-top-tracks').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: acousticness,
                backgroundColor: 'cyan',
                borderColor: [
                    ''
                ],
                borderWidth: 1
            }],
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5,
                        max: 100
                    }
                }]
            },
            title: {
                display: true,
                fontSize: '25',
                fontColor: 'white',
                text: 'Acousticness of Top Tracks'
            }
        }
    });
}

function populate_liveness_chart(audio_analysis, top_tracks) {
    let liveness = [];
    let labels = [];
    for(var i = 0; i < audio_analysis.length; i++) {
        liveness.push((audio_analysis[i]['liveness'] * 100).toFixed(0));
        labels.push(top_tracks[i]["name"]);
    }
    var ctx = document.getElementById('liveness-of-top-tracks').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: liveness,
                backgroundColor: 'pink',
                borderColor: [
                    ''
                ],
                borderWidth: 1
            }],
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        steps: 10,
                        stepValue: 5,
                        max: 100
                    }
                }]
            },
            title: {
                display: true,
                fontSize: '25',
                fontColor: 'white',
                text: 'Liveness of Top Tracks'
            }
        }
    });
}
