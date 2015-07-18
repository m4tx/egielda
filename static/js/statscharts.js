/*
 * This file is part of e-Giełda.
 * Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
 *
 * e-Giełda is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.
 */

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
        .color(['steelblue'])
        .noData(gettext("No data"));
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
        .valueFormat(d3.format('d'))
        .noData(gettext("No data"));

    d3.select("#sold-book-categories-chart svg")
        .datum(soldBookCategoriesData())
        .transition().duration(350)
        .call(chart);

    return chart;
});