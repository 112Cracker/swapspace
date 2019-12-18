from django import forms
from exchange.models import ExchangeItem, Category

MAX_ITEM_PRICE = 10000
MAX_UPLOAD_SIZE = 2500000

class ExchangeItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    def __init__(self, *args, **kwargs):
        super(ExchangeItemForm, self).__init__(*args, **kwargs)
        self.auto_id = 'id_item_%s'

    class Meta:
        model = ExchangeItem
        fields = ('name', 'category', 'description', 'price', 'image1', 'image2', 'image3')
        labels = {
            'name': 'Name',
            'category': 'Category',
            'description': 'Description',
            'price': 'Price Assessment',
            'image1': 'Add Picture',
            'image2': 'Add Additional Picture',
            'image3': 'Add Additional Picture',
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price > MAX_ITEM_PRICE:
            raise forms.ValidationError('Item too expensive for exchanging (max price is {0} dollars)'.format(MAX_ITEM_PRICE))
        return price

    def clean_image1(self):
        image = self.cleaned_data['image1']
        if image and image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('Image too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return image

    def clean_image2(self):
        image = self.cleaned_data['image2']
        if image and image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('Image too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return image

    def clean_image3(self):
        image = self.cleaned_data['image3']
        if image and image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('Image too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return image
