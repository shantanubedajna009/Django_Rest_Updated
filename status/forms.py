from django import forms


class StatusModelForm(forms.ModelForm):

    class Meta:
        fields =[
            'user',
            'content',
            'image',
        ]


    def clean_content(self, *args, **kwargs):
        data = self.cleaned_data
        content  = data.get('content', None)

        if content == "":
            content = None

        if content is not None:
            if len(content) > 240:
                raise forms.ValidationError('Content too long')
        else:
            raise forms.ValidationError('Content can\'t be empty')

        return content

    # def clean(self, *args, **kwargs):
    #     data = self.cleaned_data

    #     image = data.get('image', None)



    #     if image is None:
    #         raise forms.ValidationError("Image Required !!!!")

    #     return super().clean(*args, **kwargs)
