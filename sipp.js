(function(ext) {
    var current_step = 0;
    var init_step = 0;
    var database;
    var address;
    var way = 'USB';
    var status = 1;
    var localStored = 0;
    var localCurrent = 0;
	var ax = 0;
	var ay = 0;
	var az = 0;
	
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
            url: 'http://localhost:8080/services/pedometer/data/currentStep',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                console.log(data);
                
                
				var obj = JSON.parse(data);
                localCurrent = obj.value;
                callback(localCurrent);
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                callback(0);
            },
        });
    };
	
	ext.ax = function (callback) {
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/services/pedometer/data/ax',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                console.log(data);
                
                var obj = JSON.parse(data);
                ax = obj.value;
                callback(ax);
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                callback(0);
            },
        });
    };
	
	ext.ay = function (callback) {
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/services/pedometer/data/ay',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                console.log(data);
                
                var obj = JSON.parse(data);
                ay = obj.value;
                callback(ay);
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                callback(0);
            },
        });
    };
	
	ext.az = function (callback) {
        $.ajax({
            type: 'GET',
            url: 'http://localhost:8080/services/pedometer/data/az',
            dataType: 'jsonp',
            jsonp: 'callback',
            success: (data) => {
                console.log(data);
                
                var obj = JSON.parse(data);
                az = obj.value;
                callback(az);
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
            ['R', 'StoredCount', 'stored_step'], 
            ['R', 'CurrentCount', 'current_step'],
			['R', 'Ax', 'ax'],
			['R', 'Ay', 'ay'],
			['R', 'Az', 'az']
        ]
    };

    // Register the extension
    ScratchExtensions.register('SippSensor', descriptor, ext);
})({});