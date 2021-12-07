from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from kiteconnect import KiteConnect
from django.contrib.auth import get_user_model
from django.urls import reverse


class Order(models.Model):
    VARIETY_CHOICES = (
        ("regular", "regular"),
        ("amo", "amo"),
    )

    EXCHANGE_CHOICES = (
        ("NSE", "NSE"),
        ("NFO", "NFO"),
    )

    TRANSACTION_TYPE_CHOICES = (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
    )

    ORDER_TYPE_CHOICES = (
        ("MARKET", "MARKET"),
        ("LIMIT", "LIMIT"),
        ("SL", "SL"),
    )

    VALIDITY_CHOICES = (
        ("DAY", "DAY"),
    )

    PRODUCT_CHOICES = (
        ("MIS", "MIS"),
        ("NRML", "NRML"),
    )

    user = models.ForeignKey(get_user_model(), verbose_name=_("User"), on_delete=models.CASCADE, related_name="orders")
    variety = models.CharField(_("Variety"), max_length=15, choices=VARIETY_CHOICES, default="regular")
    exchange = models.CharField(_("Exchange"), max_length=10, choices=EXCHANGE_CHOICES, default="NFO")
    tradingsymbol = models.CharField(_("Trading Symbol"), max_length=50)
    transaction_type = models.CharField(_("Transaction Type"), max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    product = models.CharField(_("Product"), max_length=15, choices=PRODUCT_CHOICES, default="NRML")
    order_type = models.CharField(_("Order Type"), max_length=50, choices=ORDER_TYPE_CHOICES)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    validity = models.CharField(_("Validity"), max_length=15, null=True, blank=True, choices=VALIDITY_CHOICES, default="DAY")
    disclosed_quantity = models.PositiveIntegerField(_("Disclosed Quantity"), default=0)
    trigger_price = models.DecimalField(_("Trigger Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    squareoff = models.DecimalField(_("Squareoff"), max_digits=10, decimal_places=2, null=True, blank=True)
    stoploss = models.DecimalField(_("Squareoff"), max_digits=10, decimal_places=2, null=True, blank=True)
    trailing_stoploss = models.DecimalField(_("Squareoff"), max_digits=10, decimal_places=2, null=True, blank=True)
    tag = models.CharField(_("Tag"), max_length=255, null=True, blank=True)
    update = models.BooleanField(_("Update"), default=True)
    cancel = models.BooleanField(_("Cancel Order"), default=False)
    placed_by = models.CharField(_("Places By"), max_length=6, null=True, blank=True)
    order_id = models.CharField(_("Order Id"), max_length=15, null=True, blank=True)
    exchange_order_id = models.CharField(_("Exchange Order Id"), max_length=20, null=True, blank=True)
    parent_order_id = models.CharField(_("Parent Order ID"), max_length=15, null=True, blank=True)
    status = models.CharField(_("Status"), max_length=50, null=True, blank=True)
    status_message = models.TextField(_("Status Message"), null=True, blank=True)
    status_message_raw = models.TextField(_("Status Message Raw"), null=True, blank=True)
    order_timestamp = models.DateTimeField(_("Order Timestamp"), null=True, blank=True)
    exchange_update_timestamp = models.DateTimeField(_("Exchange Update Timestamp"), null=True, blank=True)
    exchange_timestamp = models.DateTimeField(_("Exchange Timestamp"), null=True, blank=True)
    instrument_token = models.BigIntegerField(default=0)
    average_price = models.DecimalField(_("Average Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    filled_quantity = models.PositiveIntegerField(_("Filled Quantity"), null=True, blank=True)
    pending_quantity = models.PositiveIntegerField(_("Pending Quantity"), null=True, blank=True)
    cancelled_quantity = models.PositiveIntegerField(_("Cancelled Quantity"), null=True, blank=True)
    market_protection = models.PositiveIntegerField(_("Market Protection"), null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)
    guid = models.CharField(_("GUID"), max_length=20, null=True, blank=True)
    

    def initialize_kite(self):
        kb = self.user.kite_broker
        self.kite = KiteConnect(api_key=kb.api_key)
        self.kite.set_access_token(access_token=kb.access_token)

    def place_order(self):
        self.order_id = self.kite.place_order(
            variety = self.variety,
            exchange = self.exchange,
            tradingsymbol = self.tradingsymbol,
            transaction_type = self.transaction_type,
            quantity = self.quantity,
            product = self.product,
            order_type = self.order_type,
            price = self.price,
            validity = self.validity,
            disclosed_quantity = self.disclosed_quantity,
            trigger_price = self.trigger_price,
            squareoff = self.squareoff,
            stoploss = self.stoploss,
            trailing_stoploss = self.trailing_stoploss,
            tag = self.tag
        )

    def modify_order(self):
        self.kite.modify_order(
            variety = self.variety,
            order_id = self.order_id,
            parent_order_id = self.parent_order_id,
            quantity = self.quantity,
            price = self.price,
            order_type = self.order_type,
            trigger_price = self.trigger_price,
            validity = self.validity,
            disclosed_quantity = self.disclosed_quantity
        )

    def cancel_order(self):
        self.kite.cancel_order(
            variety = self.variety,
            order_id = self.order_id,
            parent_order_id = self.parent_order_id
        )

    def set_status(self):
        if self.order_id:
            history = self.kite.order_history(order_id=self.order_id)[-1]
            self.placed_by = history.get('placed_by', self.placed_by)
            self.order_id = history.get('order_id', self.order_id)
            self.exchange_order_id = history.get('exchange_order_id', self.exchange_order_id)
            self.parent_order_id = history.get('parent_order_id', self.parent_order_id)
            self.status = history.get('status', self.status)
            self.status_message = history.get('status_message', self.status_message)
            self.status_message_raw = history.get('status_message_raw', self.status_message_raw)
            self.order_timestamp = history.get('order_timestamp', self.order_timestamp)
            self.exchange_update_timestamp = history.get('exchange_update_timestamp', self.exchange_update_timestamp)
            self.exchange_timestamp = history.get('exchange_timestamp', self.exchange_timestamp)
            self.average_price = history.get('average_price', self.average_price)
            self.filled_quantity = history.get('filled_quantity', self.filled_quantity)
            self.pending_quantity = history.get('pending_quantity', self.pending_quantity)
            self.market_protection = history.get('market_protection', self.market_protection)
            self.meta = history.get('meta', self.meta)
            self.tag = history.get('tag', self.tag)
            self.guid = history.get('guid', self.guid)
    
    def save(self, *args, **kwargs):
        if self.update:
            self.initialize_kite()

            if self.cancel and self.order_id:
                self.cancel_order()
            elif self.order_id:
                self.modify_order()
            else:
                self.place_order()

            self.update = False
        
        self.set_status()
        super(Order, self).save(*args, **kwargs)
    
    def __str__(self):
        if self.order_id:
            return f"{self.order_id}"
        else:
            return f"{self.pk}"


class Strategy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, related_name='strategy_user', on_delete=models.RESTRICT)
    underlying = models.CharField(max_length=20, default='BANKNIFTY')
    strategy = models.CharField(max_length=50, choices=(('straddle', 'Straddle'),('strangle', 'strangle')))
    difference = models.IntegerField(default=0)
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    stop_loss_type = models.CharField(max_length=50, choices=(('points', 'Points'),('percentage', 'Percentage')))
    stop_loss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    move_sl_to_cost = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("strategy_update", kwargs={"pk": self.pk})
    
    class Meta:
        verbose_name_plural = "strategies"

class StrategyOrder(models.Model):
    strategy = models.ForeignKey(Strategy, verbose_name=_("Strategy"), on_delete=models.CASCADE, related_name='strategy_order')
    entry_order = models.ForeignKey(Order, verbose_name=_("Entry Order"), on_delete=models.CASCADE, null=True, blank=True, related_name='entry_order')
    exit_order = models.ForeignKey(Order, verbose_name=_("Entry Order"), on_delete=models.CASCADE, null=True, blank=True, related_name='exit_order')