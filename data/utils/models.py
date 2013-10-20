def get_or_make(model, **kwargs):
    """
    Tries to get a model or make it.
    Return model, True if it exists.
    If
    """
    try:
        return model.get(**kwargs), True
    except model.DoesNotExist:
        return model(**kwargs), False