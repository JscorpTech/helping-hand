from django.conf.locale import LANG_INFO

LANG_INFO.update(
    {
        "kaa": {
            "bidi": False,  # O‘ngdan chapga yo‘nalish (False - Chapdan o‘ngga)
            "code": "kaa",
            "name": "Qaraqalpaqsha",
            "name_local": "Қарақалпақша",  # Tilning mahalliy nomi
        },
        "kril": {
            "bidi": False,  # O‘ngdan chapga yo‘nalish (False - Chapdan o‘ngga)
            "code": "kril",
            "name": "Kril",
            "name_local": "Крил",
        },
    }
)
