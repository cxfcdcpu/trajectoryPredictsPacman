var express = require('express');
var app = express();
var path = require('path');

var myLogger = function (req, res, next) {
    console.log('GET ' + req.path)
    next()
}

app.use(myLogger);
app.use(express.static('.'))
bodyParser = require('body-parser');
app.use(bodyParser.json());
const spawn= require('child_process').spawn;
// viewed at http://localhost:8080
app.get('/', function (req, res, next) {
    res.sendFile(path.join(__dirname + '/index.htm'));
});
const { exec } = require('child_process');
const http = require('http');

app.post('/predict', function(req,res){

    var resultID=req.body.nodes;
    // //console.log("simulating routing for: "+resultID + "from source node: "+ sourceNode);
    //
    // //console.log(resultID);
    // exec('python ../predict.py '+resultID, (err, stdout, stderr) => {
    //     if (err) {
    //         console.error(`exec error: ${err}`);
    //         return;
    //     }
    //     res.json(JSON.stringify({result: stdout}));
    //     console.log(`Number of files ${stdout}`);
    //
    // });
    var options = {
        host: '192.168.0.17',
        port: 5000,
        path: '/predict',
        method: 'POST'
    };
    console.log(resultID);
    if (resultID==""|| resultID==" "){
        res.send(0);
    }else{
        const rq = http.request(options, (rs) => {
            rs.on('data', (chunk) => {
                console.log(chunk.toString());
                res.json(chunk.toString())
            });
            rs.on('end', () => {
                console.log('No more data in response.');
            });
        });
        rq.on('error', (e) => {
            console.error(`problem with request: ${e.message}`);
        });
        rq.write(resultID);
        rq.end();
    }


});


var PORT = process.env.PORT || 8889;
const host = '0.0.0.0';
app.listen(PORT, host);
