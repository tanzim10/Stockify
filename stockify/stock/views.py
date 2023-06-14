from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
import pandas as pd
from . models import StockDeposit,StockList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from . import utils
from . import utils
from django.db import transaction
# Create your views here.

def stock_fetch(request):
    symbols = ['AAPL','AMZN','META','MSFT','ABNB','ADBE','PFE','ASTR','TSLA','AAL']
    data = utils.stock_fetch_api(symbols)
    context = {'data':data} 

    return render(request,'stock/stocktable.html',context)

@login_required
def buy_stock(request):
    error_message = ''
    if request.method =='POST':
        stock_name = request.POST.get('stock_name')
        amount = int(request.POST.get('amount'))
        
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
            messages.success('Successfully Purchashed!')
            return redirect('buy-stock')
        else:
            response_message = 'Not sufficient Balance!'
    else:
        messages.warning('Please use the approriate method to buy the stock!')
        return redirect('buy-stock')

    context = {'message':response_message}

    return render(request,'stock/buy_stock.html')
    
@login_required
def sell_stock(request):

    if request.method == 'POST':
        deposit_id = int(request.POST.get('deposit_id'))
        stock_deposit = get_object_or_404(StockDeposit,id =deposit_id)
        user = request.user
        with transaction.atomic():
            if stock_deposit.user == user:
                sale_price = stock_deposit.amount *stock_deposit.unit_price
                user.profile.adjust_balance(sale_price,'increment')

                stock_deposit.delete()

                return redirect('sell-stock')
            else:
                messages.warning('You are not allowed to sell this stock!')
                return redirect('sell-stock')
        
    return render(request,'stock/sell_stock.html')

def predictions(request):

    context ={}
    if request.method == 'POST':
        stock_symbol = str(request.POST.get('symbol'))
        date = str(request.POST.get('end_date'))
        results = StockList.objects.filter(symbol = stock_symbol)
        if not results:
            error_mesg = "No stocks found in this name!"
            messages.warning(error_mesg)
            return redirect('predictions')
        
        valid = utils.get_predictions(results,date)
        pred_price = utils.get_predictions(results,date)
        dates = utils.get_dates(date)

        context ={'valid':valid,
                  'price':pred_price,
                  'dates':date}
        
    
    return render(request,'stock/predictions.html',context)


        
       


        
        

        




    

   

    

