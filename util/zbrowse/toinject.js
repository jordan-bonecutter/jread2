function print_PerformanceEntries() {
  // Use getEntries() to get a list of all performance entries
  var p = performance.getEntries();
  for (var i=0; i < p.length; i++) {
    print_PerformanceEntry(p[i]);
  }
}

function print_PerformanceEntry(perfEntry) {
  console.log('!@#$!@#$'+JSON.stringify(perfEntry));
}

print_PerformanceEntries();
