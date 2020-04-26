import React, { Component } from 'react'
import { Link } from 'react-router-dom';
import Helmet from 'react-helmet'
import Main from '../layouts/Main';
import FileUpload from '../containers/FileUpload';
import CustomForm from '../containers/CustomForm';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Switch from '@material-ui/core/Switch';
import ModelSelector from '../containers/ModelSelector';
import classes from './Index.module.css';


class Index extends Component {

    state = {
      fileUpload:false
    }
    handleFileUpload = (event) =>{
        // event.preventDefault();
        const {fileUpload} = {...this.state}
        this.setState({fileUpload:!fileUpload})
    }

    render() {
      let inputMethod = null;
      if(!this.state.fileUpload){
        inputMethod = (
          <CustomForm fileUpload={this.state.fileUpload} handleFileUpload={this.handleFileUpload}/>
        )
      }else{
        inputMethod = (
          <FileUpload/>
        )
      }
      return (
        <>
          <Main>
            <Helmet  title="Home" />
            <div style={{"textAlign":"center"}}>
                {/* <img src={background} alt="background" className={classes.Image}/> */}
                <h1>Reddiec Flair Detector</h1>
                <p>Enter Submission URL(from r/India) or upload text file containing URLs to predict the flair(s)</p>
            </div>
        
            <FormGroup>
                <FormControlLabel
                    control={<Switch color="primary" checked={this.fileUpload} onChange={this.handleFileUpload} name="anythin" />}
                    label="Upload File"
                />
            </FormGroup>
            {inputMethod}
          </Main>
        </>
      )
    }
  }
  
  export default Index
  
