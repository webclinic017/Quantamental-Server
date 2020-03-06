# 通过定时任务把一些不变的数据、需要进一步加工的数据处理后存入数据库,再向数据库请求数据

import pandas as pd
import tushare as ts
import baostock as bs
from flask import jsonify

# from . import scheduler,mongo
from . import mongo


# @scheduler.task('cron',id='handle_firm_meta',hour=0) # 装饰器写法没有成功，尚不知原因
def handle_firm_meta():
    # datasource 1
    ts_df = ts.get_stock_basics()
    ts_df = ts_df.filter(items=['industry','area']) 
    
    # datasource 2
    bs_lg = bs.login()
    if bs_lg.error_msg!='success':
        print('baostock登录失败，请查明原因。')
        return 
    bs_df = bs.query_stock_basic().get_data()
    bs.logout()

    bs_df = bs_df[bs_df['type']=='1'] # 只需要股票1，排除指数2和其他3
    bs_df.drop(columns=['type'],inplace=True) # no need
    bs_df.rename(columns={'code':'stkcd','code_name':'name'},inplace=True) # 重命名，与前端保持一致
    bs_df['status'].replace({'1':'上市','0':'退市'},inplace=True) # 明确含义
    split_code = bs_df['stkcd'].str.split('.',expand=True) # sh.600000
    split_code.columns = ['market','code']
    bs_df.index = split_code['code']

    # merge
    df = pd.concat([ts_df,bs_df],axis=1)

    # transpose and to dict
    # like {
    #   '688177': {
    #       'industry': '生物制药', 
    #       'area': '广东', 
    #       'stkcd': 'sh.688177', 
    #       'code_name': '百奥泰', 
    #       'ipoDate': '2020-02-21', 
    #       'outDate': '', 
    #       'status': '上市'}
    # }
    df = df.T.to_dict()  
    # write into db
    with mongo.app.app_context():
        mongo.db.drop_collection('FirmMeta') 
        mongo.db.FirmMeta.insert_many(list(df.values())) 
    print('【job:handle_firm_meta】 执行完毕...')
