
(function(ext) {
    var current_step = 0;
    var init_step = 0;
    var database;
    var address;
    var way = 'USB';
    var status = 1;
    var localStored = 0;
    var localCurrent = 0;

    // Cleanup function when the extension is unloaded
    ext._shutdown = function() {
        database.goOffline();
        steps = 0;
        status = 1;
    };

    // Status reporting code
    // Use this to report missing hardware, plugin or unsupported browser
    ext._getStatus = function() {
        
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/services/thing/status/system',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                var obj = JSON.parse(data);
                if (obj.status === "READY") {
                    status = 2;
                } else {
                    status = 1;
                }
                msg = obj.status;
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                status = 0;
                msg = "ERROR";
            },
        });
        return {status: status, msg: msg};
    };

    ext.stored_step = function (callback) {
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/services/pedometer/data/step',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                console.log(data);
                var obj = JSON.parse(data);
                localStored = obj.value;
                callback(localStored);
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                callback(0);
            },
        });
    };

    ext.current_step = function (callback) {
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/services/pedometer/data/step',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                console.log(data);
                
                var obj = JSON.parse(data);
                if (localStored == 0) {
                    localStored = obj.value;
                }
                var localCurrent = obj.value - localStored;
                localStored = obj.value;
                callback(localCurrent);
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                callback(0);
            },
        });
    };

    // Block and block menu descriptions
    var descriptor = {
        blocks: [
            ['R', '累計步數', 'stored_step'], 
            ['R', '觸發', 'current_step'], 
            ['R', 'AccX', 'accx'], 
            ['R', 'AccY', 'accy'], 
            ['R', 'AccZ', 'accz'],
        ]
    };

    // Register the extension
    ScratchExtensions.register('SippSensor', descriptor, ext);
})({});
