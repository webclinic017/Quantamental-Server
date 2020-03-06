import os
from apscheduler.jobstores.mongodb import MongoDBJobStore

DB_URI = "mongodb+srv://{username}:{password}@freemongo-y7xk6.mongodb.net/chives?retryWrites=true&w=majority"

class Config(object):
    # app key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    #---------------------------------------
    # 配置mongoengine数据库
    # MONGODB_SETTINGS = {
    #     'db': 'chives',
    #     'host': DB_URI.format(
    #         username=os.environ.get('MONGODB_ATLAS_USERNAME'),
    #         password=os.environ.get('MONGODB_ATLAS_SECRET')),
    # }

    # --------------------------------------
    # 配置pymongo数据库
    MONGO_URI = DB_URI.format(
            username=os.environ.get('MONGODB_ATLAS_USERNAME'),
            password=os.environ.get('MONGODB_ATLAS_SECRET'))
    MONGO_DBNAME = 'chives'

    # -----------------------------------
    # 定时任务配置——此处jobs可以选择装饰器写法，参数优先级高于此处，但仍要在这里注册JOBS,id和func必须有
    JOBS = [
        {
            'id':'handle_firm_meta',
            'func':'api.jobs:handle_firm_meta',
            'args':(),
            'trigger':'cron',
            'hour':0
        }
    ]
    # 任务储存位置
    SCHEDULER_JOBSTORES={
        # 'default': SQLAlchemyJobStore(url='sqlite://')
        'mongo': MongoDBJobStore(database='chives',collection='jobs',host=MONGO_URI)
    }
    # 调度器开关
    # SCHEDULER_API_ENABLED = True
    
    # 线程池配置
    # SCHEDULER_EXECUTORS = {
    #     'default': {'type': 'threadpool', 'max_workers': 20}
    # }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False, # job积攒的次数，比如系统挂了恢复后是否执行一次，还是执行积攒次数，False：积攒次数，True：一次
        'max_instances': 1, # 同一个job同一时间最多有几个实例在运行
        'misfire_grace_time':30 # 超时容错，比如job因某种原因没有被调度，超过规定时间但在30s内，仍然会执行，超时超了30s以上就不会再执行
    }