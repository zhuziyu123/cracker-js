# https://www.389680.com/#/?shareName=&proxyAccount=  登录密码 token
import hashlib

"""
密码 md5 两次
n = E({}, e);
var a = (0,
x.default)((0,
x.default)(n.userPassword))
  , r = a.substr(0, 16)
  , o = a.substr(16)
  , l = r.split("").reverse().join("") + o.split("").reverse().join("")
  , u = l + l.substr(0, 3)
  , s = (0,
x.default)(u).toLowerCase();
n.userPassword = s,

token 
var c = (0,
x.default)((0,
x.default)(n.userAccount))
  , f = c.substr(0, 16)
  , d = c.substr(16)
  , p = f.split("").reverse().join("") + d.split("").reverse().join("")
  , m = p + p.substr(3, 6)
  , g = (0,
x.default)(m);
return n.token = g,
"""


def md5(_str):
    return hashlib.md5(_str.encode()).hexdigest()


a = md5(md5('123'))
r = a[0:16]
o = a[16:]
r1 = list(r)
r1.reverse()
o1 = list(o)
o1.reverse()
l = ''.join(r1) + ''.join(o1)
u = l + l[0:3]
s = md5(u).lower()

pwd = s

c = md5(md5('123'))
f = c[0:16]
d = c[16:]
f1 = list(f)
f1.reverse()
d1 = list(d)
d1.reverse()
p = ''.join(f1) + ''.join(d1)
m = p + p[3:9]
g = md5(m).lower()
token = g
