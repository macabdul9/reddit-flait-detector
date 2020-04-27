import React, { Component } from "react";
import { Button } from "react-bootstrap";
import Form from "react-bootstrap/Form";
import classes from "./CustomForm.module.css";
import background from "../assets/home.png";
import ModelSelector from "../containers/ModelSelector";
import axios from "axios";

import { CircularProgress } from "@material-ui/core";
import { json } from "body-parser";
import CustomizedProgressBars from './Progress';

class CustomForm extends Component {
  state = {
    submitting: false,
    value: "",
    error:false,
    responseData : "",
  };

  handleChange = (event) => {
    this.setState({ value: event.target.value });
  };

  handleSubmit = (event) => {
    //   alert('An essay was submitted: ' + this.state.value);
    event.preventDefault();
    this.setState({submitting: true});
    const { value } = { ...this.state };
    var data = {url:value}
    // console.log('data', data);
    axios.post("https://midas-rfd-api.herokuapp.com/reactRequest/", data)
      .then((res) => {
        this.setState({submitting: false, value: "" , responseData:res.data});
        // console.log(res.data);
      })
      .catch((err) => {
        // console.error(err);
        this.setState({ submitting: false, value: "",  error:true, hasResponseArrived:true, responseData:"Something went wrong"});
      });
    
  };

  render() {
    // if(this.state.error){
    //   console.log("Oops some error occured");
    // }
    let progress = null;
    if (this.state.submitting) {
      progress = <CircularProgress />;
    }
    let response = null;
    if(!this.state.error){
        response=(
          <div className={classes.parent}>
            <p className={classes.Child}><strong>Actual Flair: </strong>{this.state.responseData.flair}</p>
            <p className={classes.Child}><strong>Top-3 Flairs(with confidence value): </strong>{this.state.responseData.top_3_pred}</p>
            <p className={classes.Child}><strong>Text: </strong>{this.state.responseData.text}</p>
            <p className={classes.Child}><strong>Text Description: </strong>Title + Body + Top-10 comments ? num_comments > 10 : all comments + URL</p>
          </div>
        )
    }else if(this.state.error && this.hasResponseArrived){
      response = <p>Oops, Something went wrong, check your internet connect and/or url</p>
    }
    // console.log('flair', this.state.responseData.flair);
    return (
      <div className={classes.Top}>
        <div>
          <Form className={classes.Form} onSubmit={this.handleSubmit}>
            <Form.Group controlId="formText">
              <Form.Control
                type="text"
                value={this.state.value}
                onChange={this.handleChange}
                placeholder="Enter Submission URL"
                style={{ borderRadius: "50px" }}
              />
              <Form.Text className="text-muted" style={{ color: "red" }}>
                Please Enter a valid submission url.
              </Form.Text>
            </Form.Group>
            {/* <ModelSelector /> */}
            <Button variant="primary" type="submit" className={classes.Button}>
              Predict
            </Button>
          </Form>

          {progress}
          {response}
        </div>
      </div>
    );
  }
}

export default CustomForm;
