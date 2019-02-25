# coding: utf-8
from dns import resolver

ans = resolver.query("mysql-test.fclassroom.cn", "A")
for i in ans.response.answer:
    print(i)
    for j in i.items:
        print (j.address)
