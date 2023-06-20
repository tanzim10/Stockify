from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
import pandas as pd
from . models import StockDeposit,StockList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import utils
from django.db import transaction
import numpy as np
# Create your views here.

def stock_fetch(request):
    nasdqs = StockList.objects.all()
    tickers =[]
    for nasdq in nasdqs:
        tickers.append(str(nasdq.symbol))
    data = utils.stock_fetch_api(tickers)

    context = {'data':data} 

    return render(request,'stock/stocktable.html',context)

@login_required
def buy_stock(request):
    context ={}
    response_message =''
    nasdqs = StockList.objects.all()
    tickers =[]
    for nasdq in nasdqs:
        tickers.append(str(nasdq.symbol))
    if request.method =='POST':
        stock_name = request.POST.get('stock_name')
        amount = int(request.POST.get('amount'))
        #STOCK NAME ERROR CHECK TO be done 
        unit_price = utils.unit_price_fetch(stock_name)
        total_price = unit_price*amount
        user = request.user
        if user.profile.balance >= total_price:
            with transaction.atomic():
                stock_deposit =StockDeposit(user =request.user,
                                            stock_name = stock_name,
                                            amount = amount,
                                            unit_price =unit_price,
                                            total_price =total_price)

            stock_deposit.save()
            user.profile.adjust_balance(total_price,'decrement')
            #messages.success('Successfully Purchashed!')
            return redirect('buy-stock')
        else:
            response_message = 'Not sufficient Balance!'
    # else:
    #     context = {'message':response_message,
    #            'tickers':tickers,
    #            'symbol':'MSFT'}
    #     # messages.warning('Please use the approriate method to buy the stock!')
    #     return render(request,'stock/buy_stock.html',context)

    context = {'message':response_message,
               'tickers':tickers,
               'symbol':'MSFT'}
    
    return render(request,'stock/buy_stock.html',context)
    
@login_required
def sell_stock(request):
    context = {}
    if request.method == 'POST':
        deposit_id = int(request.POST.get('deposit_id'))
        stock_deposit = get_object_or_404(StockDeposit,id =deposit_id)
        user = request.user
        with transaction.atomic():
            if stock_deposit.user == user:
                sale_price = stock_deposit.amount *stock_deposit.unit_price
                context ={'sale_price':sale_price}
                user.profile.adjust_balance(sale_price,'increment')

                stock_deposit.delete()

                return redirect('sell-stock')
            else:
                #messages.warning('You are not allowed to sell this stock!')
                return redirect('sell-stock')
            
        
    return render(request,'stock/sell_stock.html',context)

def predictions(request):
    context ={}
    nasdqs = StockList.objects.all()
    tickers =[]
    for nasdq in nasdqs:
        tickers.append(str(nasdq.symbol))
    if request.method == 'POST':
        stock_symbol = str(request.POST.get('symbol'))
        date = str(request.POST.get('date'))
        print(date)
        print(stock_symbol)
        # if not stock_symbol:
        #     error_mesg = "No stocks found in this name!"
        #     #messages.warning(error_mesg)
        #     return redirect('predictions')
        close, predictions, pred_price = utils.get_predictions(stock_symbol,date)
        dates = utils.get_dates(date)
        print(close)
        print(predictions)
        print(dates)
        pred_price = np.array(pred_price)
        pred_value = pred_price[0][0]


        context ={'close':close,
                'predictions':predictions,
                  'price':pred_value,
                  'dates':dates,
                  'tickers':tickers}
        return render(request,'stock/predictions.html',context)
            

    context ={'tickers':tickers}
    return render(request,'stock/predictions.html',context)



       


        
        

        




    

   

    

