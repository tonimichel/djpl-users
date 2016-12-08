
def select(composer):
    from . import settings
    import django_productline.settings
    composer.compose(settings, django_productline.settings)
    # compose static files
    from . import assets
    import statics.assets
    composer.compose(assets, statics.assets)
