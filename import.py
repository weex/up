#!/usr/bin/env python3

import apsw

connection = apsw.Connection("up.db")
c = connection.cursor()

c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.249.223:12005/","jgarzik","dns" ))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.249.223:8000/","jgarzik","hashfs"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.249.223:12012/","jgarzik","fortune"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.249.223:12002/","jgarzik","apibb"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.213.110:3456","ztnark","deal or no deal"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.53.126:5000/price/coinbase","dougbit",""))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.88.105:5000/variants","joepickrell","genotype/phenotype"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.195.231:5000/","",""))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.146.248.219:5500/info","david84","stock ticker service"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.50.12:5000/","",""))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.246.239:5000/info","tyler","retweet"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.141.53:5000/info","cypherdoc","fileserver.py"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.34.100:5000/files","dsterry","fileserver.py"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.34.100:5001/info","dsterry","causeway"))
c.execute("INSERT INTO service (url, owner, name) values ( ?, ?, ? )", ( "http://10.244.209.195:5000/","justin",""))
