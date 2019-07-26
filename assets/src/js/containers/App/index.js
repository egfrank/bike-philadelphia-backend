import React from 'react';
import Title from '../../components/Title';

import { Map, Marker, Popup, TileLayer } from 'react-leaflet'

// CONSTANTS
import axios from 'axios';

import L from 'leaflet';

// delete L.Icon.Default.prototype._getIconUrl;

// L.Icon.Default.mergeOptions({
//     iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
//     iconUrl: require('leaflet/dist/images/marker-icon.png'),
//     shadowUrl: require('leaflet/dist/images/marker-shadow.png')
// });



const ENDPOINT = 'https://bike-philly.com/api/v1/stations';

function createIconImgUrl(icon){
  return `http://openweathermap.org/img/w/${icon}.png`
}

function convertKtoF(kelvin){
  return Math.round(9 /  5 * (kelvin - 273) + 32, 2)
}


function subsetInfo(stationInfo){
  const reducedStationInfo= {
    coordinates:  [stationInfo.geometry.coordinates[1], stationInfo.geometry.coordinates[0]],
    id: stationInfo.properties.kioskId,
    name: stationInfo.properties.name,
    addressStreet: stationInfo.properties.addressStreet,
    bikesAvailable:stationInfo.properties.bikesAvailable,
    totalDocks:stationInfo.properties.totalDocks,
  }
  return reducedStationInfo
}
const position = [39.95378, -75.16374];
const zoom = 13;
const mapStyle = {
    height: 900,
    width: 600,
    float: 'left',
}

const listStyle = {
    width: 400,
    float: 'right',
}

const accessToken = `pk.eyJ1IjoiZWxsaW90Z2ZyYW5rIiwiYSI6ImNqd3V4aXFzZTBkMjA0YW4xNGFwNnU4cWwifQ.BsUA_68pUHaCU7v4PCKLKw`
const id = 'mapbox.streets';
const mapboxURL = `https://api.tiles.mapbox.com/v4/${id}/{z}/{x}/{y}.png?access_token=${accessToken}`

function Weather(props){
  return (
      <div className="weather">
          <span>{props.weather.temperature}</span>
          <span><img src={props.weather.iconUrl} alt="weather icon"></img></span>
          <span>{props.weather.weather}</span>
      </div>
  )}

function MarkersList(props){
  let markersArray = Object.values(props.stations)
                        .map(s => <StationMarker key={`marker-${s.id}`} station={s} selectedStations={props.selectedStations} handleClickOnMarker={props.handleClickOnMarker}/>);
  return markersArray;
}



class StationMarker extends React.Component{
  constructor(props){
    super(props);
    this.onClickMarker = this.onClickMarker.bind(this);
  }

  onClickMarker(event){
    this.props.handleClickOnMarker(this.props.station.id);
  }


  render() {
    return (
      <Marker position={this.props.station.coordinates} id={this.props.station.id} onClick={this.onClickMarker}>
        <Popup> <h1>{this.props.station.name}</h1></Popup>
      </Marker>
      )
  }
}

class AppContainer extends React.Component{
  constructor(props){
    super(props);
    this.state = {
      stations: {},
      weather: {},
      selectedStations: [],
    };
    this.handleClickOnMarker = this.handleClickOnMarker.bind(this)
    this.handleClickOnStationInfo = this.handleClickOnStationInfo.bind(this)
  }

  handleClickOnStationInfo(stationID){
    let selectedStations = this.state.selectedStations;

    if ( selectedStations.includes(stationID) ){
      let index = selectedStations.indexOf(stationID);
        if (index > -1) {
          selectedStations.splice(index, 1);
        }
    } else {
      selectedStations.push(stationID);
    };

    this.setState({selectedStations});
  }


  handleClickOnMarker(stationID){

    let selectedStations = this.state.selectedStations;

    if ( selectedStations.includes(stationID) ){
      let index = selectedStations.indexOf(stationID);
        if (index > -1) {
          selectedStations.splice(index, 1);
        }
    } else {
      selectedStations.push(stationID);
    };

    this.setState({selectedStations});
  }


  componentDidMount(){
    axios.get(ENDPOINT)
        .then(response => response.data)
        .then(results => {
          let stations = {};
          for (const [stationID, stationInformation] of Object.entries(results.stations)){
            stations[stationID] = subsetInfo(stationInformation);
          }
          const weather = {
              temperature: convertKtoF(results.weather.main.temp) + '\xB0',
              iconUrl: createIconImgUrl(results.weather.weather[0].icon),
              weather: results.weather.weather[0].main,};
          this.setState({stations, weather});
        })
  }

  


  render(){
    return (
      <div>
      
    <Weather weather={this.state.weather}  />
    <StationsContainer stations={this.state.stations} selectedStations={this.state.selectedStations} 
        handleClickOnMarker={this.handleClickOnMarker} handleClickOnStationInfo={this.handleClickOnStationInfo}/>
    </div>
    )}
}





class StationsContainer extends React.Component{

  render(){
    return (
      <div>
          <Map center={position} zoom={zoom} style={mapStyle}>
          <TileLayer
              url={mapboxURL}
              attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"/>
          <MarkersList stations={this.props.stations} handleClickOnMarker={this.props.handleClickOnMarker} selectedStations={this.props.selectedStations}/>
          </Map>
          <div style={listStyle}>
          <h2>Stations</h2>
          <StationsList  stations={this.props.stations} handleClickOnStationInfo={this.props.handleClickOnStationInfo} selectedStations={this.props.selectedStations} />
          </div>
      </div>
  )}
}


function StationsList(props){
  let stationsList = Object.values(props.stations)
                        .map(s => <Station key={s.id} handleClickOnStationInfo={props.handleClickOnStationInfo} station={s} selectedStations={props.selectedStations}/>);
  return stationsList;
}  

class Station extends React.Component{
  constructor(props){
    super(props);
    this.clickOnStationInfo = this.clickOnStationInfo.bind(this)
  }

  clickOnStationInfo(event){
    this.props.handleClickOnStationInfo(this.props.station.id);
  }

  render(){
    if (this.props.selectedStations.includes(this.props.station.id)){
      return (
        <div>
          <h1 onClick={this.clickOnStationInfo}>{this.props.station.name}</h1>
          <div className="extended-info">
                {this.props.station.addressStreet}<div/>
                <h3>{this.props.station.bikesAvailable} / {this.props.station.totalDocks}</h3>
              </div>
        </div>
        )} else {
    return null;
  }
  }
}




class App extends React.Component {
  render () {
    const text = 'Bike Philly';
    return (
        <div className="App">
		    <Title text={text} />
		    <AppContainer/>
         </div>

    )
  }
}
export default App;
