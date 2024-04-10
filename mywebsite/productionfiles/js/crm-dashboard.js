/* Revenue Analytics Chart */
var options = {
    series: [
        {
            type: 'line',
            name: 'Profit',
            data: [
                {
                    x: 'Day1',
                    y: 432
                },
                {
                    x: 'Day2',
                    y: 352
                },
                {
                    x: 'Day3',
                    y: 800
                },
                {
                    x: 'Day4',
                    y: 1760
                },
                {
                    x: 'Day5',
                    y: 3782
                },
                {
                    x: 'Day21',
                    y: 33202
                },
                {
                    x: 'Day25',
                    y: 45034
                },
                {
                    x: 'Day30',
                    y: 60234
                },
                {
                    x: 'Day40',
                    y: 63540
                },
                {
                    x: 'Day60',
                    y: 68392
                },
                {
                    x: 'Day80',
                    y: 70502
                },
                {
                    x: 'Day100',
                    y: 88434
                }
            ]
        },
        {
            type: 'line',
            name: 'Commission',
            chart: {
                dropShadow: {
                    enabled: true,
                    enabledOnSeries: undefined,
                    top: 5,
                    left: 0,
                    blur: 3,
                    color: '#000',
                    opacity: 0.1
                }
            },
            data: [
                {
                    x: 'Day1',
                    y: 129.6
                },
                {
                    x: 'Day2',
                    y: 105.6
                },
                {
                    x: 'Day3',
                    y: 240
                },
                {
                    x: 'Day4',
                    y: 528
                },
                {
                    x: 'Day5',
                    y: 1134.5
                },
                {
                    x: 'Day21',
                    y: 9960
                },
                {
                    x: 'Day25',
                    y: 13510.5
                },
                {
                    x: 'Day30',
                    y: 18070.2
                },
                {
                    x: 'Day40',
                    y: 19062
                },
                {
                    x: 'Day60',
                    y: 20517
                },
                {
                    x: 'Day80',
                    y: 21150.6
                },
                {
                    x: 'Day100',
                    y: 26530.2
                }
            ]
        },
        {
            type: 'line',
            name: 'Spreads',
            chart: {
                dropShadow: {
                    enabled: true,
                    enabledOnSeries: undefined,
                    top: 5,
                    left: 0,
                    blur: 3,
                    color: '#000',
                    opacity: 0.1
                }
            },
            data: [
                {
                    x: 'Day1',
                    y: 30
                },
                {
                    x: 'Day2',
                    y: 30
                },
                {
                    x: 'Day3',
                    y: 30
                },
                {
                    x: 'Day4',
                    y: 30
                },
                {
                    x: 'Day5',
                    y: 30
                },
                {
                    x: 'Day21',
                    y: 30
                },
                {
                    x: 'Day25',
                    y: 30
                },
                {
                    x: 'Day30',
                    y: 30
                },
                {
                    x: 'Day40',
                    y: 30
                },
                {
                    x: 'Day60',
                    y: 30
                },
                {
                    x: 'Day80',
                    y: 30
                },
                {
                    x: 'Day100',
                    y: 30
                }
            ]
        }
    ],
    chart: {
        height: 350,
        animations: {
            speed: 500
        }
    },
    colors: ["var(--primary-color)", "rgb(69, 214, 91)", "rgb(243, 156, 18)"],
    dataLabels: {
        enabled: false
    },
    grid: {
        borderColor: '#f1f1f1',
        strokeDashArray: 3
    },
    stroke: {
        curve: 'smooth',
        width: [1, 1, 1],
    },
    xaxis: {
        axisTicks: {
            show: false,
        },
    },
    yaxis: {
        labels: {
            formatter: function (value) {
                return "£" + value;
            }
        },
    },
    tooltip: {
        y: [{
            formatter: function (e) {
                return void 0 !== e ? "£" + e.toFixed(0) : e
            }
        }, {
            formatter: function (e) {
                return void 0 !== e ? "£" + e.toFixed(0) : e
            }
        }, {
            formatter: function (e) {
                return void 0 !== e ? "£" + e.toFixed(0) : e
            }
        }]
    },
    legend: {
        show: true,
        customLegendItems: ['Profit', 'Commission', 'Spreads'],
        position: "bottom",
        offsetX: 0,
        offsetY: 8,
        markers: {
            width: 5,
            height: 5,
            strokeWidth: 0,
            strokeColor: '#fff',
            fillColors: undefined,
            radius: 12,
            customHTML: undefined,
            onClick: undefined,
            offsetX: 0,
            offsetY: 0
        },
    },
    title: {
        align: 'left',
        style: {
            fontSize: '.8125rem',
            fontWeight: 'semibold',
            color: '#8c9097'
        },
    },
    markers: {
        hover: {
            sizeOffset: 5
        }
    }
};
var chart = new ApexCharts(document.querySelector("#crm-revenue-analytics"), options);
chart.render();
/* Revenue Analytics Chart */

/* Leads By Source Chart */
var options = {
    series: [44, 55, 13, 43],
    chart: {
        width: 220,
        height: 220,
        type: "pie",
    },
    colors: ["var(--primary08)", "rgba(69, 214, 91, 0.8)", "rgba(243, 156, 18, 0.8)", "rgba(231, 76, 60, 0.8)"],
    labels: ["Mobile", "Desktop", "Laptop", "Tablet"],
    legend: {
        show: false,
    },
    stroke: {
        width: 0
    },
    dataLabels: {
        enabled: true,
        dropShadow: {
            enabled: false,
        },
    },
};
var chart1 = new ApexCharts(document.querySelector("#leads-source"), options);
chart1.render();
/* Leads By Source Chart */

/* Total Deals Chart */
var options = {
    series: [{
        name: 'Deals',
        data: [21, 22, 10, 28, 16, 21, 13, 19]
    }],
    chart: {
        height: 412,
        type: 'bar',
        events: {
            click: function (chart, w, e) {
            }
        },
        toolbar: {
            show: false,
        }
    },
    colors: ['var(--primary-color)', 'rgb(69, 214, 91)', 'rgb(243, 156, 18)', 'rgb(52, 152, 219)', 'rgb(46, 204, 113)', 'rgb(231, 76, 60)', 'rgb(0, 177, 163)', 'rgb(255, 116, 23)'],
    plotOptions: {
        bar: {
            barHeight: '2%',
            distributed: true,
            horizontal: true,
        }
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        show: false
    },
    grid: {
        borderColor: '#f1f1f1',
        strokeDashArray: 3
    },
    xaxis: {
        categories: [
            ['New Deal'],
            ['Qualified Deal'],
            ['Renewal Deal'],
            ['Referral Deal'],
            ['Won Deal'],
            ['Lost Deal'],
            ['Negotiation Deal'],
            ['Proposal/Quote'],
        ],
        labels: {
            show: false,
            style: {
                fontSize: '12px'
            },
        }
    },
    yaxis: {
        offsetX: 30,
        offsetY: 30,
        labels: {
            show: true,
            style: {
                colors: "#8c9097",
                fontSize: '11px',
                fontWeight: 600,
                cssClass: 'apexcharts-yaxis-label',
            },
            offsetY: 8,
        }
    },
    tooltip: {
        enabled: true,
        shared: false,
        intersect: true,
        x: {
            show: false
        }
    },
};
var chart2 = new ApexCharts(document.querySelector("#total-deals"), options);
chart2.render();
/* Team Deals Chart */

/* Customers By Country Map */
function mapResize() {
    var markers = [
        {
            name: "Usa",
            coords: [40.3, -101.38],
        },
        {
            name: "India",
            coords: [20.5937, 78.9629],
        },
        {
            name: "Canada",
            coords: [56.1304, -106.3468],
        },
        {
            name: "Singapore",
            coords: [1.3, 103.8],
        },
    ];
    var map = new jsVectorMap({
        map: "world_merc",
        selector: "#customers-countries",
        markersSelectable: true,
        zoomOnScroll: false,
        zoomButtons: false,

        onMarkerSelected(index, isSelected, selectedMarkers) {
            console.log(index, isSelected, selectedMarkers);
        },

        // -------- Labels --------
        labels: {
            markers: {
                render: function (marker) {
                    return marker.name;
                },
            },
        },

        // -------- Marker and label style --------
        markers: markers,
        markerStyle: {
            hover: {
                stroke: "#DDD",
                strokeWidth: 3,
                fill: "#FFF",
            },
            selected: {
                fill: "#ff525d",
            },
        },
        markerLabelStyle: {
            initial: {
                fontFamily: "Poppins",
                fontSize: 13,
                fontWeight: 500,
                fill: "#35373e",
            },
        },
    });
}
function handleResize() {
    setTimeout(() => {
        mapResize();
    }, 0);
  }
  window.addEventListener('resize', handleResize);
mapResize();

/* Customers By Country Map */


