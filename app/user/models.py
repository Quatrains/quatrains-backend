
import peewee as pw


class WxUser(pw.Model):

    union_id = pw.CharField(max_length=255)

    created_at = pw.DateTimeField()
    updated_at = pw.DateTimeField()

    class Meta:
        table_name = "wx_user"
