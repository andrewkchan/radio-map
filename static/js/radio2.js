var SCRIPT_VERSION = "104";
var map;

var socket;

var markers = []; //big ass array 
var songs = []; //format: [{bucket_location1: [{song1}, {song2}]}, {bucket_location2: [{song1}, {song2}]}]

var isDirectionsLoaded = false;
var isMapLoaded = false;
var songsProcessed = false;

var me = null;

var isPlayerLoaded = false;
var player; //youtube video player

var isExploreMode = false;


function onYouTubeIframeAPIReady() { //callback used when youtube API code downloads
  player = new YT.Player('player', {
    height: '175',
    width: '250',
    videoId: '',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
  $("iframe").hide();
}

//The YouTube API will call this function when the video player is ready.
function onPlayerReady(event) {
  isPlayerLoaded = true;
  console.log("Player ready");
  event.target.playVideo();
  processSongs(songs);
}
function onPlayerStateChange(event) {
  //func stub - TODO
}
function stopVideo() {
  player.stopVideo();
}

function getDirVec(LatLng1, LatLng2)
{
  return {lat: LatLng2.lat - LatLng1.lat, lng: LatLng2.lng - LatLng1.lng};
}
function getVecMagnitude(LatLng)
{
  return Math.sqrt(LatLng.lat * LatLng.lat + LatLng.lng * LatLng.lng)
}
function convertToLiterals(LatLngArr)
{
  //converts an array of LatLng objects to LatLng literals
  var output = [];
  for(i = 0; i < LatLngArr.length; i++)
  {
    output.push({lat: LatLngArr[i].lat(), lng: LatLngArr[i].lng()});
  }
  return output;
}

// PLAYER CLASS -----------------------------------
var UserMarker = function(marker, path) {
  this.marker = marker;
  this.image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
  this.closestSong = null;

  this.overview_path = convertToLiterals(path);
  this.overview_path_index = 0;

  this.lastWaypoint = this.overview_path[0];
  this.nextWaypoint = this.overview_path[1];
  this.directionVec = {lat: this.overview_path[1].lat - this.overview_path[0].lat, lng: this.overview_path[1].lng - this.overview_path[0].lng};
  this.speed = 0.05; //units of latitude or longitude per second

  this.timeToNextWaypoint = getVecMagnitude(this.directionVec)/this.speed * 1000;
  //MILLISECONDS to next waypoint
  this.timeSpentOnLeg = 0;

  this.currentBucket = null;
}
UserMarker.prototype.getCurrentBucket = function() {
  var latRounded = Math.round(this.marker.getPosition().lat());
  var lngRounded = Math.round(this.marker.getPosition().lng());

  var key = latRounded.toString() + "," + lngRounded.toString();
  return songs[key];
}
UserMarker.prototype.update = function(dt) {
  if(this.overview_path_index < this.overview_path.length - 1)
  {
    this.timeSpentOnLeg += dt;
    var legPercentage = this.timeSpentOnLeg/this.timeToNextWaypoint;

    if(legPercentage >= 1.0)
    {
      //get new waypoints, update time and all that
      this.overview_path_index++;
      if(this.overview_path_index < this.overview_path.length - 1)
      {
        this.lastWaypoint = this.overview_path[this.overview_path_index];
        this.nextWaypoint = this.overview_path[this.overview_path_index + 1];
        this.directionVec = {lat: this.nextWaypoint.lat - this.lastWaypoint.lat, lng: this.nextWaypoint.lng - this.lastWaypoint.lng};
        var distance = getVecMagnitude(this.directionVec);
        this.timeSpentOnLeg = 0;
        legPercentage = 0.0;
        this.timeToNextWaypoint = distance/this.speed * 1000; //MILLISECONDS
        console.log("timeToNextWaypoint:" + this.timeToNextWaypoint);
        console.log("directionvec lat:" + this.directionVec.lat);
      }
    }
    //continue on path to next waypoint
    this.marker.setPosition({lat: this.lastWaypoint.lat + this.directionVec.lat * legPercentage,
                            lng: this.lastWaypoint.lng + this.directionVec.lng * legPercentage});
  }

  //check if in new bucket
  var newBucket = this.getCurrentBucket();
  if(newBucket && newBucket != this.currentBucket)
  {
    this.currentBucket = newBucket;
    for(i = 0; i < this.currentBucket.length; i++) //if in new bucket, render new markers
    {
      addMarkerWithTimeout(parseFloat(this.currentBucket[i].lat), parseFloat(this.currentBucket[i].lng), 0, 
                            this.currentBucket[i].artistName, this.currentBucket[i].songName);
    }
  }

  //get closest song
  var newClosestSong = this.getClosestSong();
  //console.log("new closest song:" + newClosestSong.songName + ", old closestSong:" + this.closestSong.songName);
  if(newClosestSong != null && (this.closestSong == null || this.closestSong.songName != newClosestSong.songName))
  {
    console.log("Changing song!!!!");
    this.closestSong = newClosestSong;
    if(isPlayerLoaded)
    {
      player.loadVideoById(this.closestSong.youtubeLink.substring(this.closestSong.youtubeLink.indexOf("=")+1, this.closestSong.youtubeLink.length));
      $("iframe").show();
      console.log("Attempt show youtube player");
    }
  }
  //console.log(this.closestSong.songName);
}
UserMarker.prototype.getClosestSong = function() {
  //TODO
  if(this.currentBucket && this.currentBucket.length > 0)
  {
    //console.log("finding closest song");
    //console.log("song dir:" + getDirVec({lat: me.marker.getPosition().lat(), lng: me.marker.getPosition().lng()}, {lat: songs[0].lat, lng: songs[0].lng}).lng);
    var closestSong = this.currentBucket[0];
    var closestDistance = getVecMagnitude(getDirVec({lat: me.marker.getPosition().lat(), lng: me.marker.getPosition().lng()},
                                                    {lat: this.currentBucket[0].lat, lng: this.currentBucket[0].lng})
                                          );
    //console.log("closest dist:" + closestDistance);
    for(i = 0; i < this.currentBucket.length; i++)
    {
      var directionVec = getDirVec({lat: me.marker.getPosition().lat(), lng: me.marker.getPosition().lng()},
                                  {lat: this.currentBucket[i].lat, lng: this.currentBucket[i].lng});
      var distance = getVecMagnitude(directionVec);
      if(distance < closestDistance)
      {
        //console.log("closest distance:" + closestDistance);
        closestDistance = distance;
        closestSong = this.currentBucket[i];
      }
    }
    //console.log("closest song")
    return closestSong;
  }
  return null;
}
//---------------------------------------------------



//---------------------------------------------------

//callback, called when google maps API authenticates the app (see html file for where callback is input)
function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var directionsWaypoints = [];
  var request = {
    origin:{lat: 34.0522, lng: -118.2437},
    destination:{lat: 38.9072, lng: -77.0369},
    travelMode: google.maps.TravelMode.DRIVING
  };

  var customMapType = new google.maps.StyledMapType(
    [
      {
        stylers: [
          {hue: '#890000'},
          {visibility: 'simplified'},
          {gamma: 0.5},
          {weight: 0.5}
        ]
      },
      /*
      {
        elementType: 'labels',
        stylers: [{visibility: 'off'}]
      },
      */
      {
        featureType: 'water',
        stylers: [{color: '#890000'}]
      }
    ], {
      name: 'Custom Style'
  });
  var customMapTypeId = 'custom_style';

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 34.0522, lng: -118.2437},
    zoom: 8,
    draggable: false,
    disableDefaultUI: true,
    zoomControl: true,
    mapTypeControlOptions: {
      mapTypeIds: [google.maps.MapTypeId.ROADMAP, customMapTypeId]
    }
  });

  //Associate the styled map with the MapTypeId and set it to display.
  map.mapTypes.set(customMapTypeId, customMapType);
  map.setMapTypeId(customMapTypeId);


  directionsService.route(request, function(result, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      console.log("isDirectionsLoaded is changing!!!!!!!!!!!!!!!!!!!!!");
      isDirectionsLoaded = true;
      directionsWaypoints = result.routes[0].overview_path;
      console.log("path:::::"+result.routes[0].overview_path[0]);
      console.log("PROCESS LOGS!!!!!!!!!!!!!!!!!!!!!!");
      //create user, set user marker
      var marker = new google.maps.Marker({
        position: map.getCenter(),
        map: map,
        icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
      });
      me = new UserMarker(marker, directionsWaypoints);
      processSongs(songs);
    }
  });
  isMapLoaded = true;
  //processSongs(songs);
}

function addMarkerWithTimeout(lat, lng, timeout, artistName, songName) {
  window.setTimeout(function() {
    markers.push(new google.maps.Marker({
      position: {"lat": lat, "lng": lng},
      map: map,
      animation: google.maps.Animation.DROP
    }));


    markers[markers.length - 1].infoWindow = new google.maps.InfoWindow({content: "<b>" + artistName + "</b><p>" + songName + "</p>"});
    markers[markers.length - 1].infoWindow.open(map, markers[markers.length - 1]);
  }, timeout);
}

function clearMarkers() {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(null);
  }
  markers = [];
}

function processSongs(list_songs)
{
  if(list_songs.length > 0 && isMapLoaded && !songsProcessed && isPlayerLoaded && isDirectionsLoaded && !isExploreMode)
  {
    //console.log("isDirectionsLoaded:"+ isDirectionsLoaded);
    /*
    for(i = 0; i < list_songs.length; i++)
    {
      //console.log("lat:" + parseFloat(list_songs[i].lat) + ", lng:" + parseFloat(list_songs[i].lng));
      addMarkerWithTimeout(parseFloat(list_songs[i].lat), parseFloat(list_songs[i].lng), 0, list_songs[i].artistName, list_songs[i].songName);
    }
    */
    songsProcessed = true;
    startSequence();
  }
}

//add a user-specified song from the song-pin-menu onto the center of the map
function addSong()
{
  var inputArtistName = $("#artist-name-input").val();
  var inputSongName = $("#song-name-input").val();
  var inputYoutubeURL = $("#youtube-link-input").val();

  var latRounded = Math.round(map.getCenter().lat());
  var lngRounded = Math.round(map.getCenter().lng());
  var key = latRounded.toString() + "," + lngRounded.toString();

  if(inputArtistName.length > 0 && inputSongName.length > 0 && inputYoutubeURL.length > 0)
  {
    if(key in songs)
    {
      songs[key].push({"lat": map.getCenter().lat(), "lng": map.getCenter().lng(), "songName": inputSongName, 
                      "artistName": inputArtistName, "youtubeLink": inputYoutubeURL});
    }
    else
    {
      songs[key] = [{"lat": map.getCenter().lat(), "lng": map.getCenter().lng(), "songName": inputSongName, 
                      "artistName": inputArtistName, "youtubeLink": inputYoutubeURL}];
    }
    addMarkerWithTimeout(map.getCenter().lat(), map.getCenter().lng(), 0, inputArtistName, inputSongName);
  }
  else
  {
    alert("Please input text in all fields");
  }
}
//submit the user-created map
function submitMap()
{
  var inputMapName = $("#submission-name").val();

  socket.emit("check_name", {"name": inputMapName});

  socket.on("bad_submission_name",
    function(){
      alert("Please choose a different map name, that name is already in use!!!!");
    }
  );
  socket.on("ok_submission",
    function(){
      socket.emit("submit_map", {"songs": songs, "name": inputMapName});
      alert("Map submitted!!!! You are cool!!!");
    }
  );


}


$(document).ready(function() {
  main();
})

//MAIN BODY----------------------
function main() {
  $("#map-submitter").hide();
  $("#song-pin-menu").hide();
  //console.log("main loaded");
  //var socket = io.connect("http://" + document.domain + ":" + location.port + "/test");
  socket = io.connect();
  console.log("starting websocket connection");

  //send an explicit package to the server upon connection
  socket.on("connect",
    function(){
      console.log("Connection to WebSocket server being established");
      socket.emit("version_verification", {version: SCRIPT_VERSION});
    }
  );

  socket.on("choose_option",
    function(msg){
      console.log("options received");
      var maplist = msg["maps"];
      for(i = 0; i < maplist.length; i++)
      {
        $("#map-select").append($("<option></option>").val(maplist[i]).html(maplist[i]));
      }
      $("#landing-hits").click(function(){
        socket.emit("query_map", {map: $("#map-select").val()});
      });
      $("#landing-explore").click(function(){
        isExploreMode = true;
        map.set('draggable', true);
        $("#map-menu").hide();
        $("#map-submitter").show();
        $("#map-submit-btn").click(function(){submitMap();});

        $("#song-pin-menu").show();
        $("#song-add-btn").click(function(){addSong();});
      });
    }
  );

  //receive entity list
  socket.on("transmit_songs",
    function(msg){
      songs = msg["data"];
      console.log("songs received");
      $("#map-menu").hide();
      processSongs(songs);
      socket.emit("songs_received");
    }
  );

  socket.on('new_tweet',
    function(msg){
      //console.log("new tweet from WebSocket server received!");
      processTweet(msg);
    }
  );
}

function startSequence()
{
  setInterval(loop, 25);
}

function loop()
{
  if(me != null)
  {
    me.update(25);
    map.setCenter(me.marker.getPosition());
  }
}