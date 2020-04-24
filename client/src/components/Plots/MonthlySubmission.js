import React, { Component } from 'react';
import data from '../../data/plot-data/monthly_submission.json';
import Plot from 'react-plotly.js';

export class MonthlySubmission extends Component {
    const Plot = createPlotlyComponent(Plotly);
    render(){
    React.createElement(Plot, {
        data: [
        {
            type: 'scatter',
            mode: 'lines+points',
            x: [1, 2, 3],
            y: [2, 6, 3],
            marker: {color: 'red'}
        },
        {
            type: 'bar',
            x: [1, 2, 3],
            y: [2, 5, 3]
        }
        ],
        layout: {
        width: 640,
        height: 480,
        title: 'A Fancy Plot'
        }
    })

    }
}

export default MonthlySubmission
