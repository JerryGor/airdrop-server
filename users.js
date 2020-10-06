const fs = require('fs');

var alias_file = JSON.parse(fs.readFileSync('alias.json', 'utf8'))
var icons = alias_file.icons

const users = [];

const addUser = ({ id }) => {
    var iconIndex = Math.floor(Math.random() * icons.length);
    var icon = icons[iconIndex];

    const existingSameIconUser = users.find((user) => user.icon === icon);
    const username = existingSameIconUser ? icon + "-" + id.slice(0, 3) : icon

    const user = { id, username, icon }
    users.push(user)

    return { user }
}

const removeUser = ({ id }) => {
    const index = users.findIndex((user) => user.id === id);
    if (index !== -1){
        const removeUser =  users.splice(index, 1)[0]
        console.log(`Disconencting user: ${removeUser.icon}`)
        return removeUser
    }
}

const getUser = ({ id }) => {
    const user = users.find((user) => user.id === id);
    if (user){
        return user
    }
}

const getNearbyUsers = ({ id }) => {
    const nearbyUsers = users.filter((user) => {
        return ( user.id !== id)
    })
    return nearbyUsers
}

module.exports = { addUser, removeUser, getUser, getNearbyUsers };