from flask_restful import Resource, Api, reqparse, abort
from flask import jsonify
import time
from WebServerSystem.models import db, app, Item
from operator import itemgetter

"""
    api返回格式为{"status":XXX,
                  "message":XXX,
                  "data":{...}}
    添加item时，addtime和deadline的日期格式为:XXXX.XX.XX
    否则添加失败
"""

# 实例化api对象
api = Api(app)

# 实例化Paresr对象
parse = reqparse.RequestParser()

parse.add_argument('content', type=str)
parse.add_argument('status', type=int)
parse.add_argument('addtime', type=str)
parse.add_argument('deadline', type=str)


class TabrResource(Resource):
    def options(self):
        return {'Allow': '*'}, 200, {'Access-Control-Allow-Origin': '*',
                                     'Access-Control-Allow-Methods': 'HEAD, OPTIONS, GET, POST, DELETE, PUT',
                                     'Access-Control-Allow-Headers': 'Content-Type, Content-Length, Authorization, Accept, X-Requested-With , yourHeaderFeild',
                                     }


# 判断日期格式是否合法
def time_valid_or_not(date):
    try:
        time.strptime(date, "%Y.%m.%d")
        return True
    except:
        return False


# 添加时间是否在截止日期之前
def addtime_before_deadline(addtime, deadline):
    time.strptime(addtime, "%Y.%m.%d")
    time.strptime(deadline, "%Y.%m.%d")
    if deadline > addtime:
        return True
    else:
        return False


# 生成json数据响应
def return_json(status, message, data):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
    })


# 添加待办事项,只接受post请求
class AddItem(TabrResource):
    def post(self):
        # 获取post传来的数据
        args = parse.parse_args()
        content = args["content"]
        status = args["status"]
        addtime = args["addtime"]
        deadline = args["deadline"]
        # 判断日期是否合法
        if time_valid_or_not(addtime) == False or time_valid_or_not(deadline) == False:
            return return_json(1, "invalid addtime or deadline.", None)
            # 判断截止日期是否在添加日期之后
        if addtime_before_deadline(addtime, deadline) == False:
            return return_json(1, "deadline before addtime !", None)
        try:
            id_list = [item.id for item in Item.query.all()]
            # 没有事项则id从1开始
            new_id = 1
            if len(id_list) == 0:
                new_item = Item(id=new_id, content=content, status=status, addtime=addtime, deadline=deadline)
            else:
                new_id = max(id_list) + 1
                new_item = Item(id=new_id, content=content, status=status, addtime=addtime, deadline=deadline)
            db.session.add(new_item)
            db.session.commit()
            return return_json(0, "add successfully ! item_id = %d" % new_id, None)
        except Exception as e:
            print(e)
            return return_json(1, "add failed", None)

    def get(self):
        return return_json(405, "invalid method.post method only.", None)

    def put(self):
        return return_json(405, "invalid method.post method only.", None)

    def delete(self):
        return return_json(405, "invalid method.post method only.", None)


# 将待办事项设置为已完成
class Set_to_finished(TabrResource):
    def put(self, id):  # id=0 时即将所有事待办事项设置为已完成

        if id == 0:
            item_list = Item.query.filter_by(status=0).all()
            for item in item_list:
                item.status = 1
            db.session.commit()
            return return_json(0, "set all to finished successfully !", None)
        else:  # id不为0时将相应id的事项设置为已完成
            item = Item.query.filter_by(id=id).first()
            if item == None:
                abort(404, message="Item not found!")
            item.status = 1
            db.session.commit()
            return return_json(0, "set item (id = %d ) to finished successfully !" % id, None)

    def get(self):
        return return_json(405, "invalid method.put method only.", None)

    def post(self):
        return return_json(405, "invalid method.put method only.", None)

    def delete(self):
        return return_json(405, "invalid method.put method only.", None)


class Get_item(TabrResource):
    def get(self, instruction):
        data = []
        if instruction == "all":
            item_list = Item.query.all()
            for item in (item_list):
                data.append({"item_id": item.id,
                             "item_content": item.content,
                             "item_status": "待办" if item.status == 0 else "已完成",
                             "item_add_time": item.addtime,
                             "item_deadline": item.deadline})
        elif instruction == "finished":
            item_list = Item.query.filter_by(status=1).all()
            for item in item_list:
                data.append({"item_id": item.id,
                             "item_content": item.content,
                             "item_status": "已完成",
                             "item_add_time": item.addtime,
                             "item_deadline": item.deadline})
        elif instruction == "todo":
            item_list = Item.query.filter_by(status=0).all()
            for item in item_list:
                data.append({"item_id": item.id,
                             "item_content": item.content,
                             "item_status": "待办",
                             "item_add_time": item.addtime,
                             "item_deadline": item.deadline})
        else:
            abort(404, message="invalid instruction,your instruction must be"
                               " 'all' , 'todo'  or 'finished'.")
        if data != []:
            data = sorted(data, key=itemgetter("item_id"))

        return return_json(0, 'get ' + instruction + ' data' if data != [] else "No items found !", data)

    def post(self, instruction):
        return return_json(405, "invalid method.get method only.", None)

    def delete(self, instruction):
        return return_json(405, "invalid method.get method only.", None)

    def put(self, instruction):
        return return_json(405, "invalid method.get method only.", None)


# 获取事项数量
class Get_count(TabrResource):
    def get(self, instruction):
        if instruction == "all":
            num = len(Item.query.all())
        elif instruction == "finished":
            num = len(Item.query.filter_by(status=1).all())
        elif instruction == "todo":
            num = len(Item.query.filter_by(status=0).all())
        else:
            abort(404, message="invalid instruction,our instruction must be"
                               " 'all' , 'todo'  or 'finished'.")
        return return_json(0, "get '" + instruction + "' item count.", num)

    def post(self):
        return return_json(405, "invalid method.get method only.", None)

    def delete(self):
        return return_json(405, "invalid method.get method only.", None)

    def put(self):
        return return_json(405, "invalid method.get method only.", None)


# 删除某id事项
class Delete_item_by_id(TabrResource):
    def delete(self, id):
        item = Item.query.filter_by(id=id).first()
        if item == None:
            abort(404, message="Item not found!")
        db.session.delete(item)
        db.session.commit()
        return return_json(0, "delete item (id = %d) successfully !" % id, None)

    def put(self):
        return return_json(405, "invalid method.delete method only.", None)

    def post(self):
        return return_json(405, "invalid method.delete method only.", None)

    def get(self):
        return return_json(405, "invalid method.delete method only.", None)


# 删除多项事项
class Delete_item_by_instruction(TabrResource):
    def delete(self, instruction):
        items = []
        if instruction == "all":
            items = Item.query.all()
        elif instruction == "finished":
            items = Item.query.filter_by(status=1).all()
        elif instruction == "todo":
            items = Item.query.filter_by(status=0).all()
        else:
            abort(404, message="invalid instruction,our instruction must be"
                               " 'all' , 'todo'  or 'finished'.")
        count = 0
        for item in items:
            count += 1
            db.session.delete(item)
            db.session.commit()
        return return_json(0, "delete '" + instruction + "' item successfully!", {"delete_count": count}, )

    def put(self):
        return return_json(405, "invalid method.delete method only.", None)

    def post(self):
        return return_json(405, "invalid method.delete method only.", None)

    def get(self):
        return return_json(405, "invalid method.delete method only.", None)


api.add_resource(AddItem, '/add_item')
api.add_resource(Set_to_finished, '/set_to_finished/<int:id>')
api.add_resource(Get_item, '/get_item/<string:instruction>')
api.add_resource(Get_count, "/get_count/<string:instruction>")
api.add_resource(Delete_item_by_id, '/del_item_by_id/<int:id>')
api.add_resource(Delete_item_by_instruction, '/del_item_by_instruction/<string:instruction>')
