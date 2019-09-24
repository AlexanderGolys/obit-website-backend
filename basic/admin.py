from django.contrib import admin
from .models import Funeral, Obit
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


class FuneralCreationForm(forms.ModelForm):
    class Meta:
        model = Funeral
        fields = ('username', 'email', 'adress1', 'adress2', 'city', 'post_code', 'nip', 'krs', 'regon',
                  'service_info', 'equipment')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FuneralChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Funeral
        fields = ('email', 'password', 'username', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = FuneralChangeForm
    add_form = FuneralCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'adress1', 'adress2', 'city', 'post_code', 'nip', 'krs', 'regon',
                  'service_info', 'equipment')
    list_filter = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Address', {'fields': ('adress1', 'adress2', 'city', 'post_code')}),
        ('Business Info', {'fields': ('nip', 'krs', 'regon')}),
        ('Description', {'fields': ('service_info', 'equipment')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'adress1', 'adress2', 'city', 'post_code', 'nip', 'krs', 'regon')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(Funeral, UserAdmin)
admin.site.register(Obit)





