const express = require("express");
const router = express.Router();
const multer = require("multer");
const path = require('path');
const { addUser, removeUser, getUser, getNearbyUsers } = require('./users');

// Configure multer
const storage = multer.diskStorage({
    destination: function(req, file, cb) {
        cb(null, 'storage/uploads/');
    },

    // By default, multer removes file extensions so let's add them back
    filename: function(req, file, cb) {
        cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
    }
});

var upload = multer({ storage: storage })

router.get('/', (req, res) => {
    res.send('Server is up and running')
})

router.post('/upload', upload.single('file'), (req, res) => {
    const connections = req.app.locals.connections;
    const { senderId, recievers: stringfyRecievers } = req.body
    const sender = getUser({id: senderId})
    console.log(req.file)
    const { originalname, filename, size } = req.file
    const senderSocket = connections[senderId]
    const recievers = JSON.parse(stringfyRecievers);
    if (recievers.length === 0){
        senderSocket.broadcast.emit("fileSendRequest", {
            type: "fileSendRequest", 
            sender,
            originalname,
            filename,
            size,
            clicked: false,
            accepted: false
        });
    } else {
        console.log(typeof recievers)
        recievers.forEach((reciever)  => {
            const recieverSocket = connections[reciever.id];
            recieverSocket.emit("fileSendRequest", {
                type: "fileSendRequest", 
                sender,
                originalname,
                filename,
                size,
                clicked: false,
                accepted: false
            });
        })
    }

    res.send("File uploaded to server");
})

router.post('/acceptRequest', (req, res) => {
    const { request, recieverId } = req.body.data;
    const senderId = request.sender.id;
    const { originalname, filename } = request;
    res.download('storage/uploads/' + filename);
})

router.get("/acceptFile", (req, res) => {
    const { request } = req.query;

    const { filename, originalname } = JSON.parse(request)
    console.log(filename)
    res.download('storage/uploads/' + filename, originalname);
})


module.exports = router