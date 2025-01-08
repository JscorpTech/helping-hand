from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

PAGES = [
    {
        "seperator": False,
        "items": [
            {
                "title": _("Bosh sahifa"),
                "icon": "home",
                "link": reverse_lazy("admin:index"),
            }
        ],
    },
    {
        "title": _("Asosiy"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Banner"),
                "icon": "image",
                "link": reverse_lazy("admin:shared_bannermodel_changelist"),
            },
        ],
    },
    {
        "title": _("Auth"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Foydalanuvchilar"),
                "icon": "person",
                "link": reverse_lazy("admin:accounts_user_changelist"),
            },
        ],
    },
    {
        "title": "Chat",
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Guruh"),
                "icon": "group_work",
                "link": reverse_lazy("admin:chat_groupmodel_changelist"),
            },
            {
                "title": _("Xabar"),
                "icon": "sms",
                "link": reverse_lazy("admin:chat_messagemodel_changelist"),
            },
        ],
    },
    {
        "title": "Ta'lim",
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Yo'riqnomalar"),
                "icon": "menu_book",
                "link": reverse_lazy("admin:education_guidemodel_changelist"),
            },
            {
                "title": _("Imtihonlar"),
                "icon": "quiz",
                "link": reverse_lazy("admin:education_testmodel_changelist"),
            },
            {
                "title": _("O'quv qo'llanmalar"),
                "icon": "book",
                "link": reverse_lazy("admin:education_tutorialmodel_changelist"),
            },
            {
                "title": _("Savollar"),
                "icon": "question_answer",
                "link": reverse_lazy("admin:education_questionmodel_changelist"),
            },
            {
                "title": _("Javoblar"),
                "icon": "check_box",
                "link": reverse_lazy("admin:education_answermodel_changelist"),
            },
            {
                "title": _("Variantlar"),
                "icon": "shuffle",
                "link": reverse_lazy("admin:education_variantmodel_changelist"),
            },
        ],
    },
    {
        "title": _("Yangiliklar"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Postlar"),
                "icon": "article",
                "link": reverse_lazy("admin:news_postmodel_changelist"),
            },
        ],
    },
    {
        "title": _("SOS"),
        "separator": True,  # Top border
        "items": [
            {
                "title": _("Lokatsiyalar"),
                "icon": "location_on",
                "link": reverse_lazy("admin:sos_positionmodel_changelist"),
            },
            {
                "title": _("Foydalanuvchi so'rovlar"),
                "icon": "question_answer",
                "link": reverse_lazy("admin:sos_userrequestmodel_changelist"),
            },
        ],
    },
]
