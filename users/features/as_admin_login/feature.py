

def select(composer):
    from . import urls
    import django_productline.urls
    composer.compose(urls, django_productline.urls)
    

