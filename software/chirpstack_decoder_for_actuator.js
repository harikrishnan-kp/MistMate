/**
 * Decode uplink function
 * 
 * @param {object} input
 * @param {number[]} input.bytes Byte array containing the uplink payload, e.g. [255, 230, 255, 0]
 * @param {number} input.fPort Uplink fPort.
 * @param {Record<string, string>} input.variables Object containing the configured device variables.
 * 
 * @returns {{data: object}} Object representing the decoded payload.
 */
/*function decodeUplink(input) {
  return {
    data:Decode(input.fPort, input.bytes, input.variables)
  };
}
function Decode(fPort, bytes, variables) {
  var decoded={};
  decoded.status = bytes[0];
  return decoded;
  }*/


function decodeUplink(input) {
  return {
    data:Decode(input.fPort, input.bytes, input.variables)
  };
}
function Decode(fPort, bytes, variables) {
  var decoded={};
  var i = 1;
  decoded.status = bytes[i++];
  return decoded;
}


/**
 * Encode downlink function.
 * 
 * @param {object} input
 * @param {object} input.data Object representing the payload that must be encoded.
 * @param {Record<string, string>} input.variables Object containing the configured device variables.
 * 
 * @returns {{bytes: number[]}} Byte array containing the downlink payload.
 */
function encodeDownlink(input) {
  return {
    // bytes: [225, 230, 255, 0]
  };
}

