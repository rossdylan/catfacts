import tw2.core
import tw2.forms


class SubscribeForm(tw2.forms.FormPage):
    title = 'Subscribe'

    class child(tw2.forms.TableForm):
        buttons = [tw2.forms.SubmitButton(id='submit', value='Subscribe')]
        action = '/subscribe'
        id = tw2.forms.HiddenField()
        number = tw2.forms.TextField('number', label='#')


class FactForm(tw2.forms.FormPage):
    title = 'Submit a CatFact'

    class child(tw2.forms.TableForm):
        buttons = [tw2.forms.SubmitButton(id='submit', value='Cats!')]
        action = '/facts'
        id = tw2.forms.HiddenField()
        fact = tw2.forms.TextArea('fact', label='Fact')
