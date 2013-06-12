
def select(composer):
    #compose settings
    from . import settings
    import django_productline.settings
    composer.compose(settings, django_productline.settings)
    

