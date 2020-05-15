/**
 * How long to wait in ms before timing out requests to translate server.
 * @type {int}
 */
const serverTimeoutMs = 10000; // 10 seconds (chosen arbitrarily).

class Utilities {
    constructor(runtime) {
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: 'utilities',
            name: 'Browser Information',
            blocks: [
                {
		    opcode: 'getStoreCount',
                    blockType: Scratch.BlockType.REPORTER,
                    text: 'getStoreCount',
                },
		{
			opcode: 'test',
			blockType: Scratch.BlockType.REPORTER,
			text: 'getforecast',
		},
		{
			opcode: 'fuck',
			blockType: Scratch.BlockType.REPORTER,
			text: 'test',
		},
		{
			opcode: 'postmethod',
			blockType: Scratch.BlockType.REPORTER,
			text: 'postmethod',
		},
		{
			opcode: 'a01',
			blockType: Scratch.BlockType.REPORTER,
			text: 'a01',
		}
            ],
        }
    }

    getBrowserName() {
        return navigator.appVersion;
    }


	/**
	 * Get the Store Count.
	 * @return {number} - the Store Count.
	 */
	getStoreCount() {
		fetch('http://localhost:8080/services/pedometer/data/step', {
			  mode: 'cors',
			  headers: {
			    'Access-Control-Allow-Origin':'*'
			  }
			})
			.then(function(response) {
			// 處理 response
			}).catch(function(err) {
			// 錯誤處理
			});
//fetch('http://localhost:8080/services/pedometer/data/step')
	}
	
	test() {
		const Http = new XMLHttpRequest();
		const url = 'http://127.0.0.1:8080/services/pedometer/data/ax';
		Http.open("GET",url);
		Http.send();
		
		Http.onreadystatechange=(e)=>{
			console.log(Http.responseText)
		}
	}
	
	postmethod() {
		// find elements
		var $ = jQuery;
		var result = $(".result");

		$.ajax({
		 type: 'GET',
		    url: 'https://cors-anywhere.herokuapp.com/http://127.0.0.1:8080/services/pedometer/data/ax',
		    dataType: 'jsonp',
		    jsonp: 'callback',
		    success: (data) => {
			
			
            },
            err: (textStatus, errorThrown) => {
                console.log(textStatus);
                console.log(errorThrown);
                status = 0;
                msg = "ERROR";
            },
		});
		 
  
	}
	
	fuck() {
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
		    if (xhr.readyState === 4){
			console.log("response");
			console.log(xhr.responseText);
		    }
		};
		xhr.open('GET', 'https://cors-anywhere.herokuapp.com/http://127.0.0.1:8080/services/pedometer/data/ax');
		xhr.send();
	}
	
	a01() {
		var script = document.createElement('script');
		script.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
		script.type = 'text/javascript';
		document.getElementsByTagName('head')[0].appendChild(script);
		$.ajax({
			type: 'GET',
			url: 'https://cors-anywhere.herokuapp.com/http://127.0.0.1:8080/services/pedometer/data/ax',
			dataType: "JSON", // data type expected from server
			success: function (data) {
				console.log(data);
			},
			error: function(error) {
				console.log('Error: ' + error);
			}
		});
	}
	
}
Scratch.extensions.register(new Utilities());
