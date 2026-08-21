# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import pyodbc
from kiarash_cafe.settings import get_sql_connection


class User(AbstractUser):
    """مدل کاربر با اطلاعات اضافی"""
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save_to_sql(self):
        """ذخیره اطلاعات کاربر در SQL Server"""
        try:
            conn = get_sql_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO Users (username, first_name, last_name, email, phone_number, address, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.username,
                self.first_name,
                self.last_name,
                self.email,
                self.phone_number,
                self.address,
                self.password
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving to SQL: {e}")
            return False