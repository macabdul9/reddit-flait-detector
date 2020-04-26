import React, { Component } from 'react';
import Main from '../layouts/Main';
import Helmet from 'react-helmet';
// import data from '../data/plot-data/monthly_submission.json';
// import { VictoryBar } from 'victory';
// import Plotly from "plotly.js-basic-dist";
// import createPlotlyComponent from "react-plotly.js/factory";


class EDA extends Component {

    render() {

        return (
            <Main>
                <Helmet title='EDA'/>
                <h1>This is /eda route page</h1>
                <h1>Updating soon</h1>
            </Main>
        )
    }
}

export default EDA
