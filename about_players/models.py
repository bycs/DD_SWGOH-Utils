from django.db import models


class Directory(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.PositiveIntegerField(
        db_index=True,
        verbose_name='Ally Code',
    )
    player_name = models.CharField(
        db_index=True,
        max_length=100,
        verbose_name='Player Name',
    )
    telegram_username = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name='Telegram UserName',
    )
    telegram_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        verbose_name='Telegram ID',
    )
    discord_username = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name='Discord UserName',
    )
    discord_id = models.PositiveBigIntegerField(
        blank=True,
        null=True,
        verbose_name='Discord ID',
    )
    phone_number = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name='Phone Number',
    )
    username = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Directory'
        verbose_name_plural = 'Directory'

    def __str__(self):
        return self.player_name
