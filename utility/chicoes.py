from django.db import models
from django.utils.translation import ugettext as _


class A(models.IntegerChoices):
    READY = 0
    TASK_START = 1000
    ORDERS_EXPORT_START = 1001


class B(models.TextChoices):
    kk = "api.task.export.sql.queue"


ATTRIBUTION_MODEL_NAME_MAP = {
    0: _("最终互动归因"),
    2: _("先曝光后购买"),
    3: _("曝光且购买"),
    4: _("先点击后购买"),
    5: _("点击且购买"),
    6: _("全部曝光后购买归因"),
    7: _("全部点击后购买归因"),
}

a = [1, 2, 3, 4, 5, 6, 7, 8, 9]

for i in range(len(a)):

    if a[i] % 2 == 0:
        a.append(a[i])
        i -= 1
