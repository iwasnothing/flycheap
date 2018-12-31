import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import OutlinedInput from '@material-ui/core/OutlinedInput';
import FilledInput from '@material-ui/core/FilledInput';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import NativeSelect from '@material-ui/core/NativeSelect';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';
import LinearProgress from '@material-ui/core/LinearProgress';
import firebase from './Firebase';


const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 300,
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
});

class App extends Component {
  state = {
   dest: '',
   flight: [],
   to_flight: [],
   return_flight: [],
   db: null,
   loading: false,
   cities: [
{key: 'FUK', name: 'Fukuoka'},
{key: 'HIJ', name: 'Hiroshima'},
{key: 'ISG', name: 'Ishigaka'},
{key: 'KOJ', name: 'Kagoshima'},
{key: 'KMJ', name: 'Kumamoto'},
{key: 'NGS', name: 'Nagasaki'},
{key: 'NGO', name: 'Nagoya'},
{key: 'KIX', name: 'Osaka'},
{key: 'TAK', name: 'Takamatsu'},
{key: 'TYO',name: 'Tokyo'},
],
 };

 componentDidMount() {
   var db = firebase.firestore();
   var self = this
   var updatetime = null
   var timeRef = db.collection("config").doc("timestamp")
   timeRef.get().then(function(doc) {
    if (doc.exists) {
        var dic = doc.data()
        updatetime = dic['update']
        console.log("update data:", updatetime);
        self.setState({
          updatetime: updatetime,
        })
    } else {
        // doc.data() will be undefined in this case
        console.log("No such document!");
    }
    }).catch(function(error) {
        console.log("Error getting document:", error);
    });
    this.loadCities(db)

 }

 handleChange = name => event => {
   this.setState({ [name]: event.target.value, loading: true });
   console.log("select dest",event.target.value )
   this.loadData(event.target.value)
 };
 loadCities = (db) => {
   var self = this

   var list = []
   db.collection('cities').get().then(function(querySnapshot) {
        querySnapshot.forEach(function(doc) {
            // doc.data() is never undefined for query doc snapshots
            console.log("get city",doc.id);
            list.push(doc.id)
        });
        console.log("done cities")
    })
    .catch(function(error) {

        console.log("Error getting documents: ", error);
    });
 }
 loadData = (dest) => {
   var self = this
   var docRef = firebase.firestore().collection("cities").doc(dest).collection("flight").orderBy("price", "asc");
   var list = []
   docRef.get().then(function(querySnapshot) {
        querySnapshot.forEach(function(doc) {
            // doc.data() is never undefined for query doc snapshots
            console.log(doc.id, " => ", doc.data());
            var f = doc.data()
            f['key'] = doc.id
            list.push(f)
        });
        var to_flight = list.filter(f => f.return == 0).sort((a, b) =>  a.price - b.price)
        var return_flight = list.filter(f => f.return == 1).sort((a, b) =>  a.price - b.price)
        self.setState({
          flight: list,
          to_flight: to_flight,
          return_flight: return_flight,
          loading: false,
        })
    })
    .catch(function(error) {
      self.setState({
        flight: [],
        to_flight: [],
        return_flight: [],
        loading: false,
      })
        console.log("Error getting documents: ", error);
    });
 }
 render() {
    return (
      <div style={{width: 700}}>
      <Typography variant="h6" style={{witdth: 700, textAlign: 'center'}}>
      Cheapest Flight Schedule - updated on {this.state.updatetime}
      </Typography>
      <Grid container alignItems='flex-start' >
      <Grid item alignContent='center' justify='center' spacing={40}>
      <Typography variant="h6" style={{ width: 70, textAlign: 'left', marginLeft: 50, marginTop: 20}}>
      HKG  ->
      </Typography>
      </Grid>
      <Grid item>
         <FormControl style={{width: 200, marginLeft: 10}}>
           <InputLabel style={{width: 200}}>destination</InputLabel>
           <Select style={{width: 200}}
             native
             value={this.state.dest}
             onChange={this.handleChange('dest')}
             inputProps={{
               name: 'dest',
               id: 'dest-native-simple',
             }}
           >
             <option value="" />
             {this.state.cities.map((c)=> { return (<option value={c.key}>{c.name}</option>) })}

           </Select>
         </FormControl>
         </Grid>
         <Grid item alignContent='center' justify='center' spacing={40}>
         <Typography variant="h6" style={{ width: 170, textAlign: 'left', marginLeft: 50, marginTop: 20}}>
         Total fare: ${this.state.return_flight[0] == null ? 0 : this.state.to_flight[0].price + this.state.return_flight[0].price}
         </Typography>
         </Grid>
         </Grid>
{this.state.loading ? <LinearProgress />:
         <Table style={{minWidth: 700, marginLeft: 50}}>
          <TableHead>
            <TableRow>
              <TableCell>HKG -> {this.state.dest}</TableCell>
              <TableCell>{this.state.dest} -> HKG</TableCell>
              </TableRow>
            </TableHead>
             <TableBody>
             <TableRow>
             <TableCell >
      <Table style={{minWidth: 500}}>
       <TableHead>
         <TableRow>
           <TableCell>Starting Date</TableCell>
           <TableCell>Time</TableCell>
           <TableCell>Flight Code</TableCell>
           <TableCell>Price</TableCell>
         </TableRow>
       </TableHead>
       <TableBody>
       {this.state.to_flight.map(row => {
         return (
           <TableRow>
            {row.price == this.state.to_flight[0].price ?
             <TableCell component="th" scope="row" style={{backgroundColor: '#D3D3D3'}}>
               {row.date.split('T')[0]}
             </TableCell>
             :
             <TableCell component="th" scope="row" >
               {row.date.split('T')[0]}
             </TableCell>
           }
           {row.price == this.state.to_flight[0].price ?
            <TableCell component="th" scope="row" style={{backgroundColor: '#D3D3D3'}}>
              {row.date.split('T')[1]}
            </TableCell>
            :
            <TableCell component="th" scope="row" >
              {row.date.split('T')[1]}
            </TableCell>
          }
           {row.price == this.state.to_flight[0].price ?
             <TableCell style={{backgroundColor: '#D3D3D3'}}>{row.fightnum}</TableCell>
             :
             <TableCell >{row.fightnum}</TableCell>
           }
           {row.price == this.state.to_flight[0].price ?
             <TableCell style={{backgroundColor: '#D3D3D3'}}>${row.price}</TableCell>
             :
             <TableCell >${row.price}</TableCell>
           }
           </TableRow>
         );
       })}

       </TableBody>
     </Table>
            </TableCell>
            <TableCell>
            <Table style={{minWidth: 500}}>
             <TableHead>
               <TableRow>
                 <TableCell>Starting Date</TableCell>
                 <TableCell>Time</TableCell>
                 <TableCell>Flight Code</TableCell>
                 <TableCell>Price</TableCell>
               </TableRow>
             </TableHead>
             <TableBody>
             {this.state.return_flight.map(row => {
               return (
                 <TableRow>
                  {row.price == this.state.return_flight[0].price ?
                   <TableCell component="th" scope="row" style={{backgroundColor: '#D3D3D3'}}>
                     {row.date.split('T')[0]}
                   </TableCell>
                   :
                   <TableCell component="th" scope="row" >
                     {row.date.split('T')[0]}
                   </TableCell>
                 }
                 {row.price == this.state.return_flight[0].price ?
                  <TableCell component="th" scope="row" style={{backgroundColor: '#D3D3D3'}}>
                    {row.date.split('T')[1]}
                  </TableCell>
                  :
                  <TableCell component="th" scope="row" >
                    {row.date.split('T')[1]}
                  </TableCell>
                }
                 {row.price == this.state.return_flight[0].price ?
                   <TableCell style={{backgroundColor: '#D3D3D3'}}>{row.fightnum}</TableCell>
                   :
                   <TableCell >{row.fightnum}</TableCell>
                 }
                 {row.price == this.state.return_flight[0].price ?
                   <TableCell style={{backgroundColor: '#D3D3D3'}}>${row.price}</TableCell>
                   :
                   <TableCell >${row.price}</TableCell>
                 }
                 </TableRow>
               );
             })}

             </TableBody>
           </Table>
           </TableCell>
           </TableRow>
           </TableBody>
         </Table>
       }
    </div>
    );
  }
}

export default withStyles(styles)(App);
