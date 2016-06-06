# ML-for-stock-trading
1. 建立repository  
2. 建立两个branch  
3. 各自管理branch  
4. python实现Google Finance爬虫  
5. 将pandas类型的数据存储为txt  
6. 获取新的S&P 500股票代码表  
7. 获取所有的股票数据  
8. 以一支股票一个table的方式存入MySQL  
9. 访问各个table，获取股票对应的最大、最小价格和分钟平均成交量(AMV可以代替ADV)  
10. 根据最大、最小价格和AMV，已经S&P 500名单筛选出目标股票  
11. 将目标股票名单存成新的table，用来存储算法运行时的结果  
12. 实现算法实时获取特征方程(11)、(12)的结果，并做出预测存入table  
13. 根据预测结果进行实时交易操作，并将一段时间后的实际结果存入table  
14. 根据table中的预测结果与实际结果比对，结算accurary、precision、recall  
15. 周期性重复算法，不断更新三项指标，完成实验  