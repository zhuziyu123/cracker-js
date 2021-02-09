window = {
    btoa: function (str) {
        var buffer;
        if (str instanceof Buffer) {
            buffer = str;
        } else {
            buffer = Buffer.from(str.toString(), 'binary');
        }
        return buffer.toString('base64');
    },
    String: {
        fromCharCode: function (s) {
            return String.fromCharCode(s)
        }
    }
}

function S(_s) {
    return window.btoa(_s)
}

function u(n) {
    var a = "fromCharCode";
    return window.String[a](n)
}

function j(t, n) {
    t = t.split('')
    for (var a = t.length, e = n.length, r = "charCodeAt", s = 0; s < a; s++)
        t[s] = u(t[s]["charCodeAt"](0) ^ n[(s + 10) % e][r](0));
    return t.join('')
}

function analysis(url, params) {
    D = 1388
    var r = +new Date() - (D || h) - 1515125653845
        , s = ""
        , i = params;
    i = i["sort"]()["join"]("")
    i = S(i)
    console.log(i)
    i += "@#" + url.replace("https://api.qimai.cn", '')
    i += "@#" + r
    i += "@#" + 1
    console.log(i)
    s = S(j(i, "00000008d78d46a"))
    return s
}

console.log(analysis("/rank/indexPlus/brand_id/1", ['all', 'cn', 'iphone', '36', '2020-12-10', 1]))

