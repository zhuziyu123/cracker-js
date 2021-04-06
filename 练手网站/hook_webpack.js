var code_ = ""
var zzy = s;
var map_ = {};

s = function (num) {
    if (typeof (map_[num]) == "undefined") {
        map_[num] = 1;
        code_ = code_ + '"' + num + '":' + e[num] + ",";
    }
    return zzy(num);
}