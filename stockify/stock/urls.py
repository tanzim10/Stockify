from django.urls import path
from . import views

urlpatterns =[
    path('stock_table/',views.stock_fetch,name ='stock-list'),
    path('buy/',views.buy_stock,name='buy-stock'),
    path('sell/',views.sell_stock,name ='sell-stock'),
    path('predictions/',views.predictions,name ='predictions'),
    path('total_price/',views.stock_list, name='stock-total'),
    path('deposits/',views.get_deposit_id,name ='deposits'),

    


]