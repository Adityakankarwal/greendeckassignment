# python imports
import pymongo
import json
from bson.json_util import dumps
from bson import ObjectId

# restframework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# mongodb connection
con = pymongo.MongoClient('mongodb+srv://aditya:aditya@greendeck.rmjku.mongodb.net/test?retryWrites=true&w=majority')
mydb = con["greendeckassignment"]
mycol = mydb["greendeck"]

# response function
def responsedata(stat,message,data=None):

    return {
        "status":stat,
        "message":message,
        "data": data
    }

class GreendeckData(APIView):
    """
    API for Creating and Listing all data in database
    """

    # get api for listing data
    def get(self,request):

        try:
            return Response(responsedata(True, "Data Retrived", json.loads(dumps(mycol.find({})))), status=status.HTTP_200_OK)
        except:
            return Response(responsedata(False, "Could not get data"), status=status.HTTP_400_BAD_REQUEST)

    # post api for creating data
    def post(self, request):
        try:
            # get data from request
            data = request.data.get("data")

            # if data is not list
            if data is not list:
                data = [data]

            # insert list of data in database
            ids = mycol.insert_many(data)

            return Response(responsedata(True, "Data Inserted", json.loads(dumps(mycol.find({'_id':{'$in':ids.inserted_ids}})))), status = status.HTTP_200_OK)
        except Exception as e:
            return Response(responsedata(False, "Could not post data"), status = status.HTTP_400_BAD_REQUEST)


class GreendeckDataAction(APIView):
    """
    API for retrive, update, and delete data
    """

    # get single document
    def get(self, request,pk):
        try:

            # get data on basis of ID
            data = json.loads(dumps(mycol.find({'_id':ObjectId(pk)})))

            if data:
                return Response(responsedata(True, "Data Retrived",data), status=status.HTTP_200_OK)
            else:
                return Response(responsedata(True, "Data Not found"), status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response(responsedata(False, "Could not get data", str(e)), status=status.HTTP_400_BAD_REQUEST)

    # update data if present
    def put(self, request, pk):
        try:

            # get data on basis of ID
            data = json.loads(dumps(mycol.find({'_id': ObjectId(pk)})))

            # data to update
            update_data = request.data["data"]

            if data:

                # updating data
                mycol.update_one({'_id':ObjectId(pk)},{"$set":update_data})

                return Response(responsedata(True, "Data Updated", json.loads(dumps(mycol.find({'_id': ObjectId(pk)})))), status=status.HTTP_200_OK)
            else:
                return Response(responsedata(True, "Data Not found"), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(responsedata(False, "Could not get data", str(e)), status=status.HTTP_400_BAD_REQUEST)

    # Delete data
    def delete(self,request,pk):
        try:

            # get data if present
            data = json.loads(dumps(mycol.find({'_id': ObjectId(pk)})))

            if data:

                # delete data
                mycol.delete_one({'_id':ObjectId(pk)})
                return  Response(responsedata(True, "Data deleted"), status=status.HTTP_200_OK)
            else:
                return Response(responsedata(True, "Data Not found"), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(responsedata(False, "Could not get data", str(e)), status=status.HTTP_400_BAD_REQUEST)

