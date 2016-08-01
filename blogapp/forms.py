from django import forms
from .models import *
from django.contrib.auth import authenticate, get_user_model, login, logout



User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")

			if not user.is_active:
				raise forms.ValidationError("This user is not longer active.")

		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'email',
			'email2',
		]

	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email




class NewProfForm(forms.ModelForm):

	name = forms.CharField(label='Name')
	surname = forms.CharField(label='Surname')
	topic = forms.CharField(label='Topic', help_text="Select the name for your blog")

	class Meta:
		model = Profile
		fields = [
			'name',
			'surname',
			'birth_date',
			'city',
			'topic',
		]

	def clean_topic(self):
		topic = self.cleaned_data.get("topic")

		topic_qs = Profile.objects.filter(topic=topic)
		if topic_qs.exists():
			raise forms.ValidationError("This topic has already been created")
		return topic



class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = [
			"title",
			"content",
			"image",
		]


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = [
			"text",
			]


class SendMessageForm(forms.Form):

	subject = forms.CharField(max_length=25, required=True)
	email = forms.EmailField(required=True)
	message = forms.CharField(
		widget=forms.Textarea(attrs={'rows': '5', 'cols': '60',}), required=True)