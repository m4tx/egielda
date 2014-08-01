function createSimpleBarChart() {
    // I literally have no idea why NVD3.js does not provide any kind of simple bar chart...
    return nv.models.discreteBarChart()
        .x(function (d) {
            return d.label
        })
        .y(function (d) {
            return d.value
        })
        .staggerLabels(true)
        .tooltips(false)
        .showValues(true)
        .transitionDuration(350)
        .color(['steelblue']);
}

// Sold book amounts chart
nv.addGraph(function () {
    var chart = createSimpleBarChart();
    chart.yAxis.tickFormat(d3.format('d'));
    chart.valueFormat(d3.format('d'));

    d3.select('#sold-book-amounts-chart svg')
        .datum(soldBookAmountsData()) // Data provided in the HTML file
        .call(chart);
    nv.utils.windowResize(chart.update);

    return chart;
});

// Given book amounts chart
nv.addGraph(function () {
    var chart = createSimpleBarChart();
    chart.yAxis.tickFormat(d3.format('d'));
    chart.valueFormat(d3.format('d'));

    d3.select('#given-book-amounts-chart svg')
        .datum(givenBookAmountsData()) // Data provided in the HTML file
        .call(chart);
    nv.utils.windowResize(chart.update);

    return chart;
});

// Sold book prices chart
nv.addGraph(function () {
    var chart = createSimpleBarChart();

    d3.select('#sold-book-prices-chart svg')
        .datum(soldBookPricesData()) // Data provided in the HTML file
        .call(chart);
    nv.utils.windowResize(chart.update);

    return chart;
});

// Book sold by categories
nv.addGraph(function () {
    var chart = nv.models.pieChart()
        .x(function (d) {
            return d.label
        })
        .y(function (d) {
            return d.value
        })
        .showLabels(true)
        .valueFormat(d3.format('d'));

    d3.select("#sold-book-categories-chart svg")
        .datum(soldBookCategoriesData())
        .transition().duration(350)
        .call(chart);

    return chart;
});