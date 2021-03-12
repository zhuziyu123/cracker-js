// callback.js
var o = function () {
    for (var e = "qwertyuiopasdfg$hjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM", t = "", n = 0; n < 10; n++)
        t += e.charAt(~~(Math.random() * e.length));
    return t
}();

function getCallback() {
    return o;
}
