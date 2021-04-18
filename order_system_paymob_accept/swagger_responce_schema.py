""""""""""""""""""""""""""""""
# api Response Schema
""""""""""""""""""""""""""""""

def createResponseSchema(serializer):
    return {201: serializer(many=False), 422: 'Unprocessable entity'}


def updateResponseSchema(serializer):
    return {201: serializer(many=False),
            404: "Id is not exist or deleted from the database", 422: 'Unprocessable entity'}


def recordsResponseSchema(serializer):
    return {200:  serializer(many=True)}


def listResponseSchema(serializer):
    return {200:  serializer(many=True)}


def recordResponseSchema(serializer):
    return {200: serializer(many=False),
            404: "Id is not exist or deleted from the database"}


def deleteResponseSchema():
    return {200: 'Records data'}

