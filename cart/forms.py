from django import forms


class AddressForm(forms.Form):
    country = forms.ChoiceField(
        choices=[
            ("India", "India"),
        ],
        widget=forms.Select(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    address1 = forms.CharField(
        max_length=255,
        required=True,
        label="Address Line 1",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    postal_code = forms.CharField(
        max_length=10,
        required=True,
        label="Postal code",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        label="City",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    state = forms.CharField(
        max_length=100,
        required=True,
        label="State",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
    phone_number = forms.CharField(
        max_length=100,
        required=True,
        label="Phone_number",
        widget=forms.TextInput(
            attrs={"class": "w-full border-b border-gray-300 focus:outline-none p-2"}
        ),
    )
