import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import ListSubheader from '@material-ui/core/ListSubheader';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
}));

export default function GroupedSelect() {
  const classes = useStyles();

  return (
    <div>
      <FormControl className={classes.formControl}>
        <InputLabel htmlFor="grouped-select">Select Models</InputLabel>
        <Select defaultValue="" id="grouped-select">
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <ListSubheader>Models</ListSubheader>
          <MenuItem value={1}>Model 1</MenuItem>
          <MenuItem value={2}>Model 2</MenuItem>
          <MenuItem value={3}>Model 3</MenuItem>
          <MenuItem value={4}>Model 4</MenuItem>
          <MenuItem value={4}>Model 4</MenuItem>
        </Select>
      </FormControl>
    </div>
  );
}