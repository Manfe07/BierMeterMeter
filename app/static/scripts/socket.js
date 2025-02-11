export var socket = io();

export var wsData = {
    device: NaN,
    latency: NaN,
    timeDif: NaN,
    action: NaN,
    lane: NaN,
    value: NaN
};


export var watchDog = {
    pingInterval: 5000,
    ping_time: NaN,
    pong_time: NaN,
    connectionTimeout: NaN,
    online: false,
    customFunction: function (x) { }
};



socket.on('connect', function () {
    console.log("Socket: Connected")
    ping();
});


socket.on("connect_error", (err) => {
    console.log(`connect_error due to ${err.message}`);
});


function setConnectionState(state) {
    if (state) {
        clearTimeout(watchDog.connectionTimeout);
        watchDog.connectionTimeout = setTimeout(setConnectionState, (watchDog.pingInterval + 500), false);
    }

    // request actual Values when connection changes to online
    if (watchDog.online != state) {
        watchDog.online = state;
        watchDog.customFunction(state);
        if(watchDog.online)
            socket.emit('get_stopwatch', { device: wsData.device });
    }
}


function ping() {
    watchDog.ping_time = new Date().valueOf();
    socket.emit('ping', {
        data: {
            ping_time: watchDog.ping_time
        }
    });
    setTimeout(ping, watchDog.pingInterval);
}


socket.on('pong', function (msg, cb) {
    setConnectionState(true);
    watchDog.pong_time = new Date().valueOf();
    wsData.latency = (watchDog.pong_time - watchDog.ping_time) / 2;
    wsData.timeDif = (watchDog.ping_time + wsData.latency) - (msg.pong * 1000);
    console.debug({ "wsData_Latency": wsData });
});




console.log("socket.js loaded");
