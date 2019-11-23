/**
 * Created by xj on 2019/11/11.
 * chartParams.chartData  必传
 */

var echartPie = function () {
    var chartParams = {
        chartData: arguments[0].chartData,
        totalData: arguments[0].totalData ? arguments[0].totalData : {name: '', value: ''},
        isLegend: arguments[0].isLegend ? arguments[0].isLegend : false,
        isLine: arguments[0].isLine=='false' ? false : true,
        legend: arguments[0].legend ? arguments[0].legend : '',
        radius: arguments[0].radius ? arguments[0].radius : ['45%', '60%'],
        colors: arguments[0].colors ? arguments[0].colors : ['#34CED3', '#EB7153', '#2ABB9C', '#FAAA49', '#00DCFD', '#9385DD', '#0BA3B5', '#E05F35',],
    };
    var label = {};
    var labelLine = {};
    if (chartParams.isLine) {
        labelLine = {
            normal: {
                show: true,
                length: 14,
                length2: 10,
                lineStyle: {
                    type: 'dashed',
                    width: 2
                }
            }
        };
        label = {
            normal: {
                formatter: '{b|{b}}\n{hr|}\n{d|{c} ( {d}% )}',
                rich: {
                    b: {
                        fontSize: 16,
                        color: '#fff',
                        align: 'left',
                        padding: 4
                    },
                    hr: {
                        borderColor: '#12EABE',
                        width: '100%',
                        borderWidth: 2,
                        height: 0
                    },
                    d: {
                        fontSize: 16,
                        color: '#fff',
                        align: 'left',
                        padding: 4
                    },
                    c: {
                        fontSize: 16,
                        color: '#fff',
                        align: 'center',
                        padding: 4
                    }
                }
            }
        }
    } else {
        labelLine = {
            normal: {
                show: true,
                length: 0,
                length2: 10,
                lineStyle: {
                    width: 0
                }
            }
        };
        label = {}
    }
    var option = {
        legend: {
            show: chartParams.isLegend,
            data: chartParams.legend,
            center: 'center',
            textStyle: {
                color: '#fff',
                fontSize:16
            },
            itemWidth: 10,
            itemHeight: 10,
        },
        title: {
            text: chartParams.totalData.name,
            subtext: chartParams.totalData.value == 0 ? '' + chartParams.totalData.value : Number(chartParams.totalData.value) >= 1000 ? (Number(chartParams.totalData.value) / 1000).toFixed(1) + ' k' : chartParams.totalData.value,
            x: 'center',
            y: 'center',
            textStyle: {
                fontWeight: 'normal',
                fontSize: 18,
                color: '#fff',
            },
            subtextStyle: {
                fontWeight: 'normal',
                fontSize: 22,
                color: '#fff',
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{b}: <br/>{c} ({d}%)'
        },
        color: chartParams.colors,
        series: [
            {
                name: '',
                type: 'pie',
                radius: chartParams.radius,
                center: ['50%', '55%'],
                avoidLabelOverlap: true,
                label:label,
                labelLine:labelLine,
                data: chartParams.chartData
            }
        ]
    };
    return option;
};

