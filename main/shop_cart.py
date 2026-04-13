from .models import Manual


class shop_cart:
    def __init__(self, request,):
        self.request = request
        self.session = request.session

        shop_cart = self.session.get("shop-cart")
        
        if not shop_cart:
            self.session["shop-cart"] = {}
            self.shop_cart = self.session.get("shop-cart")

        else:
            self.shop_cart = shop_cart

    def add(self, manual_id):
        manual = Manual.objects.get(id=manual_id)
        manual_id_str = str(manual_id)

        if manual_id_str in self.shop_cart:
            self.shop_cart[manual_id_str]['quantity'] += 1
        
        else:
            self.shop_cart[manual_id_str] = {
                'name': manual.name,
                'price': str(manual.price),
                'imge': manual.image.url if manual.image else '',
                'quantity': 1,
            }

        self.session.modified = True

    def remove(self, manual_id):
        manual_id_str = str(manual_id)

        if manual_id_str in self.shop_cart:
            del self.shop_cart[manual_id_str]
            self.session.modified = True
    
    def get_total(self):
        return sum(
            float(item['price'] * item['quantity'])
            for item in self.shop_cart.values()
        )

    def clear(self):
        self.session['shop-cart'] = {}
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.shop_cart.values())
    
    def get_total(self):
        items = []
        for manual_id, item_data in self.shop_cart.items():
            item = item_data.copy()
            item['id'] = manual_id
            items.append(item)
        return items