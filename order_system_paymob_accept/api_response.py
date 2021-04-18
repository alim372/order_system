
def prepare_response(meta=[], data=[], state=True):

    if (state == True):
        respond = {"meta": meta, "data": data}
    elif (meta['status'] == 404):
        meta['message'] = "Record not found"
        meta['details'] = "Id is not exist or deleted from the database"
        data = {"id": ["Id is not exist or deleted from the database"]}
        respond = {"meta": meta, "errors": data}
    elif (meta['status'] == 422):
        meta['message'] = "Unprocessable entity"
        respond = {"meta": meta, "errors": data}
    else:
        respond = {"meta": meta, "errors": data}
    return respond
