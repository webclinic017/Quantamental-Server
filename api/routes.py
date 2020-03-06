from flask import url_for
from . import create_app,mongo

app = create_app()


# REST API
# -----------查询公司代码和名称------------
@app.route("/fundamental/finance/firmcodes")
def get_all_firm_code_names():
    code_names = mongo.db.FirmMeta.find({},['stkcd','name'])
    print(code_names.count())
    res = []
    if code_names is not None:
        for codename in code_names:
            codename.pop('_id')
            res.append(codename) # type(codename)=> dict
        return dict(msg='success',data=res)
    return dict(msg='failed',data=res)



#--------------------------------
# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db,firm_meta=FirmMeta)

# with app.test_request_context():
#     print(url_for('get_all_firm_code_names'))

