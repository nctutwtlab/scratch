const BlockType = require('../../extension-support/block-type');
const nets = require('nets');
const log = require('../../util/log');

/**
 * How long to wait in ms before timing out requests to translate server.
 * @type {int}
 */
const serverTimeoutMs = 10000; // 10 seconds (chosen arbitrarily).

class Scratch3NCTU {
    constructor(runtime) {
        this.runtime = runtime;
    }

    getInfo() {
        return {
            id: 'nctu',
            name: 'Browser Information',
            blocks: [
                {
                    opcode: 'getBrowserName',
                    blockType: BlockType.REPORTER,
                    text: 'Get Browser Name',
                },
				{
						opcode: 'getStoreCount',
						blockType: BlockType.REPORTER,
						text: 'StoreCount',
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
		const StoreCountPromise = new Promise(resolve => {
			nets({
				url: 'http://localhost:8080/services/pedometer/data/step',
				timeout: serverTimeoutMs
			}, (err, res, body) => {
				if (err) {
					log.warn(`get response fail`);
					resolve('');
					return '';
				}
				const data = JSON.parse(body).result;
				const storeCount = data.value
				return storeCount;
			});

		});
	}
}

module.exports = Scratch3NCTU;