import React from 'react';
import Main from '../layouts/Main';
import Helmet from 'react-helmet';
import ReportRenderer from '../render/ReportRenderer';

const Report = () => {
  return (
    <Main>
        <Helmet title="Report" />
        <ReportRenderer/>
    </Main>
  )
}

export default Report
