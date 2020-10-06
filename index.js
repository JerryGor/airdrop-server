const express = require('express');
const socketio = require('socket.io');
const http = require('http')
const cors = require('cors');
const bodyParser = require('body-parser');
const router = require('./router');

const { addUser, removeUser, getUser, getNearbyUsers } = require('./users');

// Configure server
const app = express();
const httpServer = http.createServer(app);
const io = socketio(httpServer);

// Configure express
app.use(bodyParser.json())
app.use(cors());
app.use(router);

// Configure static path
app.use(express.static(__dirname + '/storage'));

// Configure socket storage
app.locals.connections = {}

// io endpoints
io.on('connection', (socket) => {
    socket.on('join', (callback) => {
        console.log(`New connection: ${socket.id}`)
        const user = addUser({ id: socket.id })
        app.locals.connections[socket.id] = socket // Add socket to local socket storage
        socket.emit("userInfo", user)
        socket.broadcast.emit("newNearbyUser", user); // Update nearby user data for other connections

        const nearbyUsers = getNearbyUsers({ id: socket.id })
        socket.emit("nearbyUserData", nearbyUsers); // Get nearby user data for current connection

        socket.emit("welcomeMessage", {
            request:{
                type: "welcome",
                id: "admin",
                title: "Airdrop Admin",
                message: "Welcome to Airdrop.\n 1.Click nearby users to start sharing file \n 2. Send file to all nearby users if no user is selected"
            }
        })
        callback()
    })
    socket.on('fileAccepted', ({ request, recieverId, status }) => {
        const reciever = getUser({ id: recieverId });
        const senderSocket = app.locals.connections[request.sender.id];
        senderSocket.emit('fileAcceptedByNearbyUser', {
            message: `${recieverId} have accepted ${request.originalname}`,
            request:{
                type: "fileAcceptedRequest",
                reciever: reciever,
                originalname: request.originalname
            }
        });
        console.log(`${recieverId} have accepted ${request.originalname} from ${request.sender.id}`);
    })

    socket.on('fileRejected', ({ request, recieverId, status }) => {
        const reciever = getUser({ id: recieverId });
        const senderSocket = app.locals.connections[request.sender.id];
        senderSocket.emit('fileRejectedByNearbyUser', {
            message: `${recieverId} have rejected ${request.originalname}`,
            request:{
                type: "fileRejectedRequest",
                reciever: reciever,
                originalname: request.originalname
            }
        });
        console.log(`${recieverId} have rejected ${request.originalname} from ${request.sender.id}`);
    })

    socket.on('disconnect', () => {
        delete app.locals.connections[socket.id]
        const user = removeUser({ id: socket.id })
        if (user){
            console.log(user)
            socket.broadcast.emit("nearbyUserLeft", user);
        }
    })
})

// Configure listen ports
const PORT = process.env.PORT || 3006;
httpServer.listen(PORT, () => {
    console.log(`Server has started on port: ${PORT}`);
})