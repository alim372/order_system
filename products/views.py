from django.shortcuts import render
from rest_framework.parsers import  MultiPartParser, FormParser, JSONParser
from rest_framework import viewsets
from rest_framework.decorators import parser_classes, api_view, permission_classes, authentication_classes, action
from django.db import IntegrityError, transaction
from django.conf import settings
from django.db.models import Q, F, FloatField
from django.db.models import Sum
import requests
# api response 
from rest_framework.response import Response
from order_system_paymob_accept.api_response import prepare_response
# serializers
from .serializers import ProductSerializer, UserProductSerializer
# models
from .models import Product, UserProduct, StatusChoices
# authorization
from order_system_paymob_accept.middleware.authorization import administrator, user 
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from order_system_paymob_accept.swagger_responce_schema import *
""""""""""""""""""""""""""""""""""""""""""
# products controller for admin permission.
""""""""""""""""""""""""""""""""""""""""""
class Products(viewsets.ModelViewSet):
    permission_classes = [administrator]
    parser_classes = [JSONParser, MultiPartParser]
   
    @ swagger_auto_schema(
        tags=(['products - admin control']),
        responses=recordsResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['GET'])
    def records(self, request):
        """
        List all products.
        """
        # GET total records
        items = Product.objects.all()
        total = items.count()
        # create pegnation [ start record ]
        start = ((0 if ('page' not in request.GET)
                  else int(request.GET['page']) - 1)) * settings.PER_PAGE
        # create pegnation [ end record ]
        end = start + settings.PER_PAGE

        # sort update
        if 'order' in request.GET:
            if request.GET['order'].find('asc') != -1:
                order = "-" + request.GET['order'].split('.')[0]
            else:
                order = request.GET['order'].split('.')[0]
        else:
            # if not order data will order by ID DESC
            order = '-id'

        # multi search for the data
        if 'search' in request.GET and len(request.GET['search'].split(',')) >= 1:
            # Turn list of values into list of Q objects
            # return Response(request.GET['search'].split(','))
            queries = [Q(name__contains=value)
                       for value in request.GET['search'].split(',')]
            # Take one Q object from the list
            initQuery = queries.pop()
            # Or the Q object with the ones remaining in the list
            for query in queries:
                initQuery |= query
            items = items.filter(initQuery)

        # GET all records from the table with order and pegnation
        items = items.order_by(order)[start:end]

        serializer = ProductSerializer(items, many=True)
        # return the data
        return Response(prepare_response({"total": total, "count": settings.PER_PAGE, "page":   1 if ('page' not in request.GET) else request.GET['page']}, serializer.data))

    @ swagger_auto_schema(
        tags=(['products - admin control']),
        responses=recordResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['GET'])
    def record(self, request, id=None):
        """
        GET Product by id .
        """
        # GET records from table
        item = Product.objects.filter(id=id).first()

        if item:
            serializer = ProductSerializer(item, many=False)
            return Response(prepare_response({"total": 1}, serializer.data))
        # if record not found
        else:
            return Response(prepare_response({"status": 404, "instance": request.get_full_path()}, {}, False), 404)

    @ swagger_auto_schema(
        tags=(['products - admin control']),
        # responses=recordResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['GET'])
    def get_total_revenue(self, request ):
        """
        GET total products revenue.
        """
        raw_items_data = UserProduct.objects.all().values('product_id').annotate(revenue=Sum(F('count') * F('product__price_eur'), output_field=FloatField()))
        items = raw_items_data.annotate(purchased_count=F('count'), name=F('product__name'), price_eur=F('product__price_eur'))
        total_revenue = sum(raw_items_data.values_list('revenue', flat=True))
        if raw_items_data :
            return Response(prepare_response({}, {"total_revenue_eur":total_revenue, "details": items}))
        else:
            return Response(prepare_response({}, {"total_revenue_eur":0, "details": []}))

    @ swagger_auto_schema(
        tags=(['products - admin control']),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'price_eur': openapi.Schema(type=openapi.TYPE_NUMBER),
            }, required=["name", "price_eur"],
        ),
        responses=createResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['POST'])
    @ transaction.atomic
    def create(self, request):
        """
        create new products.
        """
        item = Product()
        # create all from post
        for attr, value in request.data.items():
            # if field is allowed
            if attr not in Product.protected():
                setattr(item, attr, value)
        try:
            with transaction.atomic():
                # save data
                item.save()
                # GET new data
                serializer = ProductSerializer(item, many=False)
                # retuen new data
                return Response(prepare_response({"total": 1}, serializer.data), 201)

        except Exception as error:
           
            # return valiation error
            return Response(prepare_response({"status": 422, "instance": request.get_full_path()}, error, False), 422)

    @ swagger_auto_schema(
        tags=(['products - admin control']),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'price_eur': openapi.Schema(type=openapi.TYPE_NUMBER)
            }, required=["name", "price_eur"],
        ),
        responses=createResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['PUT'])
    @ transaction.atomic
    def update(self, request, id=None):
        """
        update Product by id .
        """
        # GET records from table
        item = Product.objects.get(id=id)
        if item:
            # update all from post
            for attr, value in request.data.items():
                # if field is allowed
                if attr not in Product.protected():
                    setattr(item, attr, value)
            try:
                with transaction.atomic():
                    # save data
                    item.save()
                    # GET new data
                    serializer = ProductSerializer(item, many=False)
                    # retuen new data
                    return Response(prepare_response({"total": 1}, serializer.data), 201)
            except Exception as error:
                # return valiation error
                return Response(prepare_response({"status": 422, "instance": request.get_full_path()}, error, False), 422)
        # if record not found
        else:
            return Response(prepare_response({"status": 404, "instance": request.get_full_path()}, {}, False), 404)

    @ swagger_auto_schema(
        tags=(['products - admin control']),
        responses=deleteResponseSchema()
    )
    @ action(detail=True, methods=['DELETE'])
    @ transaction.atomic
    def delete(self, request, id=None):
        """
        delete Product by id .
        """
        # GET records from table
        item = Product.objects.filter(id=id).first()
        if item:
            with transaction.atomic():
                # delete record
                Product.objects.filter(id=id).update(
                    status=StatusChoices.DELETED)

                return Response(prepare_response({"total": 0}, {}), 201)
        # if record not found
        else:
            return Response(prepare_response({"status": 404, "instance": request.get_full_path()}, {}, False), 404)

""""""""""""""""""""""""""""""""""""""""""
# Products functions for user permission.
""""""""""""""""""""""""""""""""""""""""""
class UserProducts(viewsets.ModelViewSet):
    permission_classes = [user]
    parser_classes = [JSONParser]
    @ swagger_auto_schema(
        tags=(['products - user\'s apis']),
        responses=recordsResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['GET'])
    def records(self, request, currency=None):
        """
        List all products to normal users.
        """
        # GET total records
        items = Product.objects.all()
        total = items.count()
        # create pegnation [ start record ]
        start = ((0 if ('page' not in request.GET)
                  else int(request.GET['page']) - 1)) * settings.PER_PAGE
        # create pegnation [ end record ]
        end = start + settings.PER_PAGE

        # sort update
        if 'order' in request.GET:
            if request.GET['order'].find('asc') != -1:
                order = "-" + request.GET['order'].split('.')[0]
            else:
                order = request.GET['order'].split('.')[0]
        else:
            # if not order data will order by ID DESC
            order = '-id'

        # multi search for the data
        if 'search' in request.GET and len(request.GET['search'].split(',')) >= 1:
            # Turn list of values into list of Q objects
            # return Response(request.GET['search'].split(','))
            queries = [Q(name__contains=value)
                       for value in request.GET['search'].split(',')]
            # Take one Q object from the list
            initQuery = queries.pop()
            # Or the Q object with the ones remaining in the list
            for query in queries:
                initQuery |= query
            items = items.filter(initQuery)

        # GET all records from the table with order and pegnation
        items = items.order_by(order)[start:end]

        serializer = ProductSerializer(items, many=True)
        # use fixer for conversion
        if currency != None:
            headers = {'Content-type': 'application/json'}
            fixer_response = requests.get(settings.FIXER_BASE_URL+'latest?'+'access_key='+settings.FIXER_ACCESS_KEY, headers=headers)
            if (fixer_response.status_code == 200):
                currencies = fixer_response.json()['rates']
                if currency in currencies :
                    for row in serializer.data:
                        row['user_currancy_price'] = row['price_eur'] * currencies[currency]
                
        # return the data
        return Response(prepare_response({"total": total, "count": settings.PER_PAGE, "page":   1 if ('page' not in request.GET) else request.GET['page']}, serializer.data))
    
    @ swagger_auto_schema(
        tags=(['products - user\'s apis']),
        responses=recordsResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['GET'])
    def purchased_records(self, request, currency=None):
        """
        List all purchased products to normal users.
        """
        # GET total records
        items = UserProduct.objects.filter(user=request.user).all()
        total = items.count()
        # create pegnation [ start record ]
        start = ((0 if ('page' not in request.GET)
                  else int(request.GET['page']) - 1)) * settings.PER_PAGE
        # create pegnation [ end record ]
        end = start + settings.PER_PAGE
        order = '-id'
        # GET all records from the table with order and pegnation
        items = items.order_by(order)[start:end]

        serializer = UserProductSerializer(items, many=True)
        # use fixer for conversion
        if currency != None:
            headers = {'Content-type': 'application/json'}
            fixer_response = requests.get(settings.FIXER_BASE_URL+'latest?'+'access_key='+settings.FIXER_ACCESS_KEY, headers=headers)
            if (fixer_response.status_code == 200):
                currencies = fixer_response.json()['rates']
                if currency in currencies :
                    for row in serializer.data:
                        row['product']['user_currancy_price'] = row['product']['price_eur'] * currencies[currency]
                else:
                    return Response(prepare_response({"status": 422, "instance": request.get_full_path()}, {}, False), 422)
        # return the data
        return Response(prepare_response({"total": total, "count": settings.PER_PAGE, "page":   1 if ('page' not in request.GET) else request.GET['page']}, serializer.data))

    @ swagger_auto_schema(
        tags=(['products - user\'s apis']),
        responses=recordResponseSchema(ProductSerializer)
    )
    @ action(detail=True, methods=['GET'])
    def record(self, request, id=None, currency=None):
        """
        GET Product by id .
        """
        # GET records from table
        item = Product.objects.filter(id=id).first()

        if item:
            item = ProductSerializer(item, many=False).data
            if currency != None:
                headers = {'Content-type': 'application/json'}
            fixer_response = requests.get(settings.FIXER_BASE_URL+'latest?'+'access_key='+settings.FIXER_ACCESS_KEY, headers=headers)
            if (fixer_response.status_code == 200):
                currencies = fixer_response.json()['rates']
                if currency in currencies :
                    item['user_currancy_price'] = item['price_eur'] * currencies[currency]
            return Response(prepare_response({"total": 1}, item))
        # if record not found
        else:
            return Response(prepare_response({"status": 404, "instance": request.get_full_path()}, {}, False), 404)

    @ swagger_auto_schema(
        tags=(['products - user\'s apis']),
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            }, required=["product_id"],
        ),
        responses=createResponseSchema(UserProductSerializer)
    )
    @ action(detail=True, methods=['POST'])
    @ transaction.atomic
    def purchase(self, request):
        """
        purchase new products.
        """
        data = request.data
        try:
            with transaction.atomic():
                # update or create data
                item, created = UserProduct.objects.update_or_create(
                    product_id=data['product_id'], user=request.user 
                )
                if not created :
                    item.count +=1
                    item.save()
                # GET new data
                serializer = UserProductSerializer(item, many=False)
                # retuen new data
                return Response(prepare_response({"total": 1}, serializer.data), 201)

        except Exception as error:
            # return valiation error
            return Response(prepare_response({"status": 422, "instance": request.get_full_path()}, error, False), 422)
