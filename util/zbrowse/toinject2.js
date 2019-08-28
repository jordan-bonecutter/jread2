function calculate_load_times() {
  // Check performance support
  if (performance === undefined) {
    return;
  }

  // Get a list of "resource" performance entries
  var resources = performance.getEntriesByType("resource");
  if (resources === undefined || resources.length <= 0) {
    return;
  }
  for (var i=0; i < resources.length; i++) {
    // Redirect time
    var info = {name: resources[i].name};
    var t = resources[i].redirectEnd - resources[i].redirectStart;
    info.redirect_time = t;
    // DNS time
    t = resources[i].domainLookupEnd - resources[i].domainLookupStart;
    info.dns_lookup_time = t;
    // TCP handshake time
    t = resources[i].connectEnd - resources[i].connectStart;
    info.tcp_time = t;
    // Secure connection time
    t = (resources[i].secureConnectionStart > 0) ? (resources[i].connectEnd - resources[i].secureConnectionStart) : "0";
    info.secure_connection_time = t;
    // Response time
    t = resources[i].responseEnd - resources[i].responseStart;
    info.response_time = t;
    // Fetch until response end
    t = (resources[i].fetchStart > 0) ? (resources[i].responseEnd - resources[i].fetchStart) : "0";
    info.fetch_until_response_end_time = t;
    // Request start until reponse end
    t = (resources[i].requestStart > 0) ? (resources[i].responseEnd - resources[i].requestStart) : "0";
    info.request_start_to_response_end = t;
    // Start until reponse end
    t = (resources[i].startTime > 0) ? (resources[i].responseEnd - resources[i].startTime) : "0";
    info.start_to_response_end = t;
    console.log('!@#$!@#$'+JSON.stringify(info));
  }
}

calculate_load_times();
