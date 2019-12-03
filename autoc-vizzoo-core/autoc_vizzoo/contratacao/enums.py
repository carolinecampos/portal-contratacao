from djchoices import DjangoChoices, ChoiceItem

class TipoTemplateEmail(DjangoChoices):
    confirmacao_adiquirentes = ChoiceItem('confirmacao_adiquirentes')