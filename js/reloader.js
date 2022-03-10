
// https://livecodestream.dev/post/5-ways-to-make-http-requests-in-javascript/
function call(mod, on_load, args="")
{
    //create XMLHttpRequest object
    const xhr = new XMLHttpRequest();
    //open a get request with the remote server URL
    xhr.open("GET", "http://"+window.location.host.split(":")[0]+":4500/SuckMyLegApis/"+mod+"/?"+args);
    //send the Http request
    xhr.send();

    //EVENT HANDLERS

    //triggered when the response is completed
    xhr.onload = function() {
      if (xhr.status === 200) {
        data = JSON.parse(xhr.responseText);
        return data;
      } else if (xhr.status === 404) {
        console.log("No records found");
      }
    }

    //triggered when a network-level error occurs with the request
    xhr.onerror = function() {
      console.log("Network error occurred");
    }

    //triggered periodically as the client receives data
    //used to monitor the progress of the request
    xhr.onprogress = function(e) {
      if (e.lengthComputable) {
        console.log(`${e.loaded} B of ${e.total} B loaded!`);
      } else {
        console.log(`${e.loaded} B loaded!`);
      }
    }
}

// https://livecodestream.dev/post/5-ways-to-make-http-requests-in-javascript/
function reload(mod, on_load, args="")
{
    //create XMLHttpRequest object
    const xhr = new XMLHttpRequest();
    //open a get request with the remote server URL
    xhr.open("GET", "http://"+window.location.host.split(":")[0]+":4500/SuckMyLegApis/"+mod+"/?"+args);
    //send the Http request
    xhr.send();

    //EVENT HANDLERS

    //triggered when the response is completed
    xhr.onload = function() {
      if (xhr.status === 200) {
        data = JSON.parse(xhr.responseText);
        on_load(data);
      } else if (xhr.status === 404) {
        console.log("No records found");
      }
    }

    //triggered when a network-level error occurs with the request
    xhr.onerror = function() {
      console.log("Network error occurred");
    }

    //triggered periodically as the client receives data
    //used to monitor the progress of the request
    xhr.onprogress = function(e) {
      if (e.lengthComputable) {
        console.log(`${e.loaded} B of ${e.total} B loaded!`);
      } else {
        console.log(`${e.loaded} B loaded!`);
      }
    }
}

//https://www.tutorialspoint.com/javascript-sleep-function
function sleep(ms) 
{
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function auto_reload(server, code, fun, delay=1000)
{
  while (true)
  {
    reload(server, fun, code);
    await sleep(delay)
  }
}