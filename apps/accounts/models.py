# apps/accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
import pyodbc
from kiarash_cafe.settings import get_sql_connection


class User(AbstractUser):
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
            if conn is None:
                print("❌ اتصال به SQL Server برقرار نشد!")
                return False

            cursor = conn.cursor()

            # ایجاد جدول اگر وجود نداشت
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
                BEGIN
                    CREATE TABLE Users (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        username NVARCHAR(150) UNIQUE NOT NULL,
                        first_name NVARCHAR(100) NOT NULL,
                        last_name NVARCHAR(100) NOT NULL,
                        email NVARCHAR(255) UNIQUE NOT NULL,
                        phone_number NVARCHAR(15) UNIQUE NOT NULL,
                        address NVARCHAR(MAX) NOT NULL,
                        password NVARCHAR(255) NOT NULL,
                        created_at DATETIME DEFAULT GETDATE(),
                        updated_at DATETIME DEFAULT GETDATE()
                    )
                END
            """)
            conn.commit()

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
            print(f"✅ کاربر {self.username} در SQL Server ذخیره شد!")
            return True

        except pyodbc.IntegrityError as e:
            print(f"❌ خطای یکتایی (تکراری): {e}")
            return False
        except Exception as e:
            print(f"❌ خطا در ذخیره در SQL Server: {e}")
            return False

    # ===== اضافه کردن این متد =====
    def update_in_sql(self):
        """به‌روزرسانی اطلاعات کاربر در SQL Server"""
        try:
            conn = get_sql_connection()
            if conn is None:
                print("❌ اتصال به SQL Server برقرار نشد!")
                return False

            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Users 
                SET first_name = ?,
                    last_name = ?,
                    email = ?,
                    phone_number = ?,
                    address = ?,
                    password = ?,
                    updated_at = GETDATE()
                WHERE username = ?
            """, (
                self.first_name,
                self.last_name,
                self.email,
                self.phone_number,
                self.address,
                self.password,
                self.username
            ))
            conn.commit()

            cursor.close()
            conn.close()
            print(f"✅ کاربر {self.username} در SQL Server به‌روزرسانی شد!")
            return True

        except Exception as e:
            print(f"❌ خطا در به‌روزرسانی SQL Server: {e}")
            return False