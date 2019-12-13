# Bitcoinparser
tools for parse the bitcoin local data,it works very well 

It offers three methods ,you can choose by youself:


learn more :[解析原理博客总结](https://blog.csdn.net/boke14122621/article/details/103162435)


(1)本地rpc的方法：
https://www.jianshu.com/p/514512224e68
 
 ```
bitcoind -damon  
 
bitcoin-cli -rpcconnect=127.0.0.1 -rpcuser=rpc -rpcpassword=123  getblock  00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048 
 ```
 
(2)  直接读取  
了解区块数据结构即可，参考 https://github.com/rigmarole/blk-reader
 
(3) 借用工具 
https://github.com/alecalve/python-bitcoin-blockchain-parser
 
 
(4) 借助API
https://github.com/blockchain/api-v1-client-python
 
(5) 其他
一个好用的工具bitiodine：
 
https://github.com/mikispag/bitiodine
 
 
bitcoin数据分析：
     https://github.com/citp/BlockSci
