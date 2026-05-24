from django import forms  # 修正這裡：刪除錯誤的 TrueForm 導入

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label='數量')
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CouponApplyForm(forms.Form):
    code = forms.CharField(label='折扣碼')