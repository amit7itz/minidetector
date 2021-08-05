from minidetector.database import Entity, create_session
from flask import Flask
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow

app = Flask("minidetector-api")
api = Api(app)
ma = Marshmallow(app)

class EntitySchema(ma.Schema):
    class Meta:
        fields = ("id", "mac", "ip")

class AllResources(Resource):
    def get(self):
        session = create_session()
        app.logger.info(f"Resouce: {self.__class__.__name__} - Session had been created")
        query = session.query(Entity).all()
        session.close()
        app.logger.info(f"Resouce: {self.__class__.__name__} - Session had been closed")
        app.logger.info(entitiesSchema.dump(query))
        return entitiesSchema.dump(query)

class GetRouteMac(Resource):
    def get(self):
        sql_stmt = f'''
        select mac from {Entity.__tablename__} group by mac having count(*) > 3; 
        '''
        app.logger.info(f"Resouce: {self.__class__.__name__} - SQL Statement: {sql_stmt}")
        session = create_session()
        app.logger.info(f"Resouce: {self.__class__.__name__} - Session had been created")
        query = session.execute(sql_stmt)
        session.close()
        app.logger.info(f"Resouce: {self.__class__.__name__} - Session had been closed")

        return entitiesSchema.dump(query)

entitiesSchema = EntitySchema(many=True)

api.add_resource(AllResources, "/all")
api.add_resource(GetRouteMac, "/route")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
