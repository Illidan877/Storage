/**
 * Created by xj on 2019/11/11.
 * chartParams.chartData  必传
 */

var echartLine = function () {
    var chartParams = {
        chartData: arguments[0].chartData,
        colors: arguments[0].colors ? arguments[0].colors : [ '#FFBA5F','#03E0F2'],
    };
    var option = {
        grid: {
            left: 20,
            right: 20,
            top: 30,
            bottom: 20,
            containLabel: true
        },
        dataZoom: [
            {
                show: false,
                realtime: true,
                start: 0,
                end: 60,
                height: 16
            },
            {
                type: 'inside',
                realtime: true,
                start: 0,
                end: 60,
                height: 16
            }
        ],
        xAxis: {
            type: 'category',
            data: chartParams.chartData.xAxisData,
            triggerEvent: true,
            splitLine: {
                show: false
            },
            axisLine: {
                show: true,
                lineStyle: {
                    width: 1,
                    color: '#29405F'
                }
            },
            axisLabel: {
                color: '#fff',
                fontSize:'16'
            },
        },
        yAxis: {
            nameTextStyle: {
                color: '#fff',
            },
            max: (rst) => {
                return Number(rst.max) + Math.ceil(rst.max / 10);
            },
            type: 'value',
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#29405F',
                    type: 'dashed'
                }
            },
            axisLine: {
                show: true,
                lineStyle: {
                    width: 1,
                    color: '#29405F'
                }
            },
            axisTick: {
                show: true
            },
            axisLabel: {
                color: '#fff',
                fontSize:'16'
            },
        },
        series: [{
            data: chartParams.chartData.data,
            type: 'line',
            symbol: 'circle',
            symbolSize: 14,
            color: chartParams.colors[0],
            lineStyle: {
                color:chartParams.colors[1],
            },
            label: {
                show: true,
                position: 'top',
                textStyle: {
                    color: chartParams.colors[0],
                    fontSize: 18,
                }
            },
            areaStyle: {
                color: 'rgba(1,98,133,0.6)'
            }
        }, {
            type: 'bar',
            animation: false,
            barWidth: 3,
            hoverAnimation: false,
            data: chartParams.chartData.data,
            tooltip: {
                show: false
            },
            itemStyle: {
                normal: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: '#91EAF2'
                        }, {
                            offset: 1,
                            color: '#074863'
                        }],
                        globalCoord: false
                    },
                    label: {
                        show: false
                    }
                }
            }
        }]
    };
    return option;
};

