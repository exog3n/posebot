exports.webServer = function() {

  var http = require('http').createServer(handler); //require http server, and create server with function handler()
  var https = require('https');
  var fs = require('fs'); //require filesystem module

  var path = require('path');
  var express = require('express');
  var app = express();
  app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
  });

  app.get('/socket.io.js', function(req, res) {
    res.sendFile(path.join(__dirname + '/socket.io.js'));
  });

  // app.get('/lib/tf.min.js', function(req, res) {
  //   res.sendFile(path.join(__dirname + '/lib/tf.min.js'));
  // });
  //
  // app.get('/lib/posenet.min.js', function(req, res) {
  //   res.sendFile(path.join(__dirname + '/lib/posenet.min.js'));
  // });
  //
  // app.get('/lib/dat.gui.js', function(req, res) {
  //   res.sendFile(path.join(__dirname + '/lib/dat.gui.js'));
  // });
  //
  // app.get('/camera.js', function(req, res) {
  //   res.sendFile(path.join(__dirname + '/camera.js'));
  // });
  //
  // app.get('/demo_util.js', function(req, res) {
  //   res.sendFile(path.join(__dirname + '/demo_util.js'));
  // });

  app.get('/posenet.js', function(req, res) {
    res.sendFile(path.join(__dirname + '/posenet.js'));
  });

  app.get('/nodebot.js', function(req, res) {
    res.sendFile(path.join(__dirname + '/nodebot.js'));
  });


  // load web server with socket.io
  const mosca = require('./mqtt_broker.js');
  let iotServer = mosca.broker();

  // var server = https.createServer({
  //   key: fs.readFileSync('./example.key'),
  //   cert: fs.readFileSync('./example.crt'),
  //   requestCert: false,
  //   rejectUnauthorized: false
  // }, handler);
  var server = https.createServer({
      key: fs.readFileSync('./example.key'),
      cert: fs.readFileSync('./example.crt'),
      requestCert: false,
      rejectUnauthorized: false
    }, app)
    .listen(8080, function() {
      console.log('Example app listening on port 8080! Go to https://localhost:8080/')
    })

  server.listen(8080); //listen to port 8080
  var io = require('socket.io').listen(server);

  function handler(req, res) { //create server
    fs.readFile(__dirname + '/index.html', function(err, data) { //read file index.html in public folder
      if (err) {
        res.writeHead(404, {
          'Content-Type': 'text/html'
        }); //display 404 on error
        return res.end("404 Not Found");
      }
      res.writeHead(200, {
        'Content-Type': 'text/html'
      }); //write HTML
      res.write(data); //write data from index.html
      return res.end();
    });
  }

  // const commands = ['pose', 'gps'];
  // let fc = 0;

  // simple socket.io
  io.sockets.on('connection', function(socket) { // WebSocket Connection
    let prvData = null;
    socket.on('pose', function(data) { //get light intensity status from client
      prvData = resController('pose', data, prvData);
    });
    socket.on('gps', function(data) {
      prvData = resController('gps', data, prvData);
    });
  });

  function resController(cmd, data, prvData) {
    let curData = data;
    if (curData) {
    // if (curData && prvData) {
    //   if (curData!= 'null' && !isEquivalent(curData, prvData)) {
        // mosca.sendMessage(iotServer, commands[fc], curData, 'l');
        // mosca.sendMessage(iotServer, commands[fc], curData, 'r');
        if(cmd=='pose'){
          mosca.sendMessage(iotServer, cmd, curData, 'l');
          mosca.sendMessage(iotServer, cmd, curData, 'r');
        }else if (cmd=='gps')
          mosca.sendMessage(iotServer, cmd, curData);
        return curData;
      }
    //   }
    // }
    // return prvData;
  }

  // function isEquivalent(a, b) {
  //   // Create arrays of property names
  //   var aProps = Object.getOwnPropertyNames(a);
  //   var bProps = Object.getOwnPropertyNames(b);
  //
  //   // If number of properties is different,
  //   // objects are not equivalent
  //   if (aProps.length != bProps.length) {
  //     return false;
  //   }
  //
  //   for (var i = 0; i < aProps.length; i++) {
  //     var propName = aProps[i];
  //
  //     // If values of same property are not equal,
  //     // objects are not equivalent
  //     if (a[propName] !== b[propName]) {
  //       return false;
  //     }
  //   }
  //
  //   // If we made it this far, objects
  //   // are considered equivalent
  //   return true;
  // }


  return io;
};
