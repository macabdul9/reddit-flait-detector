import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Helmet from 'react-helmet';
import ReactMarkdown from 'react-markdown';
import Main from '../layouts/Main';
import source from '../data/about.md';

class About extends Component {
  render() {
    const {about} = {...this.state};
    return (
      <>
        <Main>
          <Helmet title='Readme'/>
          <h1>This is /about route page</h1>
          <h1>I will update this page soon</h1>
      </Main>
      </>
    )
  }
}

export default About;
