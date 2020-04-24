import React, { Component } from 'react';
import Main from '../layouts/Main';
import Helmet from 'react-helmet';
// import data from '../data/plot-data/monthly_submission.json';
import { MonthlySubmission } from '../components/Plots/MonthlySubmission';
// import { VictoryBar } from 'victory';
// import Plotly from "plotly.js-basic-dist";
// import createPlotlyComponent from "react-plotly.js/factory";


class EDA extends Component {
    state = { 
        line1: {
           x: [-3, -2, -1],
           y: [1, 2, 3],
           name: 'Line 1' 
        },
        line2: {
           x: [1, 2, 3],
           y: [-3, -2, -1],
           name: 'Line 2'
        }
     }
    render() {
        const Plot = createPlotlyComponent(Plotly);

        return (
            <Main>
                <Helmet title='EDA'/>
                <MonthlySubmission/>
                <h1>This is /eda route page</h1>
            </Main>
        )
    }
}

export default EDA
