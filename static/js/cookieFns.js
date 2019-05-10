var cookieFns = (function() {
  function setCookies(k, v, exDays = 1) {
    /* cookie = {k:v} */
    // Set expiration
    var d = new Date();
    d.setTime(d.getTime() + exDays * 24 * 60 * 60 * 1000);
    var expires = 'expires=' + d.toUTCString();
    // Set the cookie
    document.cookie = k + '=' + v + ';' + expires + ';path=/';
  }

  function getCookies(key) {
    // Which cookie
    var name = key + '=';

    // Handle special characters
    var decodedCookie = decodeURIComponent(document.cookie);

    // Generate array of cookies if more than one
    var cookiesArr = decodedCookie.split(';');

    // Find the cookie we're looking for, return it
    for (var i = 0; i < cookiesArr.length; i++) {
      var c = cookiesArr[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }

    // No match found
    return '';
  }

  return {
    set: setCookies,
    get: getCookies,
  };
})();
