from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import Question, QuestionOptions, QuestionSet

User = get_user_model()



### Login Form.
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg',
                                                                           'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg',
                                                                                   'placeholder': 'Enter password'}))

### Register Form.
class RegistrationForm(forms.ModelForm):
    '''A form for creating new users. Includes all required fields plus
    repeated password'''
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm password'}))
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Name'}))

    class Meta:
        model = User
        fields = ['name','email',]
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter Email'})}

    def clean_password2(self):  # checking that the two passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True): # save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.is_active = True
            user.roles_id = 2
            user.save()
        return user

### Question Set Form.
class QuestionSetForm(forms.ModelForm):
    name = forms.CharField(label='Question Set Name')
    negative_marking_percentage = forms.IntegerField(label='Negative Marking Percentage', required=False)
    ideal_timeto_complete = forms.IntegerField(label='Ideal Timeto Complete')

    STATUS_CHOICES =(
    (False, False),
    (True, True),
    )

    enable_negative_marking = forms.ChoiceField(choices = STATUS_CHOICES)
    
    class Meta:
        model = QuestionSet
        fields = ['name','enable_negative_marking','negative_marking_percentage', 'ideal_timeto_complete']
    def __init__(self, *args, **kwargs):
        super(QuestionSetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
    

#### Questions Form #####
class QuestionForm(forms.ModelForm):
    text = forms.CharField(label='Question Name', required=False)
    marks = forms.IntegerField(label='Question Mark')
    order = forms.IntegerField(label='Question Order')
    class Meta:
        model = Question
        fields = ['question_set','text','image','marks','order','type']
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'

        self.fields['question_set'].required = True

#### Add Questions Options Form ####

class QuestionOptionsForm(forms.ModelForm):
    order = forms.IntegerField(label='Order')
    STATUS_CHOICES =(
    (False, False),
    (True, True),
    )

    answer = forms.ChoiceField(label='Answer',choices = STATUS_CHOICES)
    class Meta:
        model = QuestionOptions
        fields = ['question','text','image','order','answer']

    def __init__(self, *args, **kwargs):
        super(QuestionOptionsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'

        self.fields['question'].required = True

 
        