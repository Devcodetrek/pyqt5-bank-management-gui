# =============================================================
#                     DEVCODETREK BANKASI (YiGit ERDOGAN) main
# =============================================================

import sys
import pandas as pd
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

# =============================================================
#                   BANKA VERİ SİSTEMİ (LOGIC)
# =============================================================

class BankSystem:
    def __init__(self, file_name="bank_accounts.xlsx"):
        self.file_name = file_name
        if os.path.exists(self.file_name):
            self.df = pd.read_excel(self.file_name, dtype={"AccountNumber": int, "Password": str})
        else:
            self.df = pd.DataFrame(columns=["AccountNumber", "OwnerName", "Balance", "Password"])
            self.df.to_excel(self.file_name, index=False)

    def save(self):
        self.df.to_excel(self.file_name, index=False)

    def authenticate(self, account_number, password):
        password = str(password).strip()
        match = self.df[
            (self.df["AccountNumber"] == account_number) &
            (self.df["Password"].astype(str) == password)
        ]
        return not match.empty

    def create_account(self, owner_name, password):
        account_number = random.randint(10000, 99999)
        while account_number in self.df["AccountNumber"].values:
            account_number = random.randint(10000, 99999)
        new_account = {
            "AccountNumber": account_number,
            "OwnerName": owner_name,
            "Balance": 0.0,
            "Password": str(password)
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_account])], ignore_index=True)
        self.save()
        return account_number

    def deposit(self, account_number, amount, password):
        if not self.authenticate(account_number, password):
            raise ValueError("Şifre hatalı.")
        if amount <= 0:
            raise ValueError("Tutar pozitif olmalıdır.")
        idx = self.df.index[self.df["AccountNumber"] == account_number][0]
        self.df.at[idx, "Balance"] += amount
        self.save()

    def withdraw(self, account_number, amount, password):
        if not self.authenticate(account_number, password):
            raise ValueError("Şifre hatalı.")
        idx = self.df.index[self.df["AccountNumber"] == account_number][0]
        if self.df.at[idx, "Balance"] < amount:
            raise ValueError("Yetersiz bakiye.")
        self.df.at[idx, "Balance"] -= amount
        self.save()

    def check_balance(self, account_number, password):
        if not self.authenticate(account_number, password):
            raise ValueError("Şifre hatalı.")
        balance = self.df[self.df["AccountNumber"] == account_number]["Balance"].values[0]
        return balance

    def apply_interest_to_all(self, rate=0.01):
        self.df["Balance"] = self.df["Balance"] * (1 + rate)
        self.save()

    def list_accounts(self):
        return self.df[["AccountNumber", "OwnerName", "Balance"]]

    def delete_account(self, account_number, password):
        if not self.authenticate(account_number, password):
            raise ValueError("Şifre hatalı.")
        self.df = self.df[self.df["AccountNumber"] != account_number]
        self.save()

    def update_password(self, account_number, old_password, new_password):
        if not self.authenticate(account_number, old_password):
            raise ValueError("Eski şifre hatalı.")
        idx = self.df.index[self.df["AccountNumber"] == account_number][0]
        self.df.at[idx, "Password"] = new_password
        self.save()

# =============================================================
#                   GİRİŞ VE KAYIT PANELİ
# =============================================================

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Giriş Yap - DevcodeTrek Bankası")
        self.setGeometry(300, 300, 300, 250)
        self.bank = BankSystem()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Hesap No")
        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("Şifre")
        self.pw_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Giriş Yap")
        login_btn.clicked.connect(self.login)

        layout.addWidget(QLabel("Hesap No"))
        layout.addWidget(self.acc_input)
        layout.addWidget(QLabel("Şifre"))
        layout.addWidget(self.pw_input)
        layout.addWidget(login_btn)

        layout.addWidget(QLabel("Veya Yeni Hesap Oluştur"))
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText("Ad Soyad")
        self.new_pass = QLineEdit()
        self.new_pass.setPlaceholderText("Yeni Şifre")
        self.new_pass.setEchoMode(QLineEdit.Password)
        create_btn = QPushButton("Hesap Oluştur")
        create_btn.clicked.connect(self.create_account)

        layout.addWidget(self.new_name)
        layout.addWidget(self.new_pass)
        layout.addWidget(create_btn)

        self.setLayout(layout)

    def login(self):
        try:
            acc_text = self.acc_input.text().strip()
            pw = self.pw_input.text().strip()

            if not acc_text or not pw:
                QMessageBox.warning(self, "Uyarı", "Hesap numarası ve şifre boş olamaz.")
                return

            acc = int(acc_text)

            if self.bank.authenticate(acc, pw):
                self.hide()
                self.window = BankApp(account_number=acc, password=pw)
                self.window.show()
            else:
                QMessageBox.warning(self, "Hatalı Giriş", "Hesap numarası veya şifre yanlış.")
        except ValueError:
            QMessageBox.critical(self, "Hata", "Geçerli bir hesap numarası girin.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def create_account(self):
        try:
            name = self.new_name.text().strip()
            pw = self.new_pass.text().strip()
            if not name or not pw:
                QMessageBox.warning(self, "Uyarı", "Ad ve şifre boş olamaz.")
                return
            acc_no = self.bank.create_account(name, pw)
            QMessageBox.information(self, "Başarılı", f"Hesap oluşturuldu! Hesap No: {acc_no}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

# =============================================================
#                    BANKA İŞLEMLERİ PANELİ
# =============================================================

class BankApp(QWidget):
    def __init__(self, account_number, password):
        super().__init__()
        self.account_number = account_number
        self.password = password
        self.setWindowTitle("🏦 DevcodeTrek Bankası")
        self.setGeometry(100, 100, 700, 600)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.bank = BankSystem()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logo = QLabel()
        pixmap = QPixmap("logo.jpeg")
        pixmap = pixmap.scaledToHeight(80)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title = QLabel("🏦 DevcodeTrek Bankası")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        user_label = QLabel(f"👤 Oturum Açan Hesap: {self.account_number}")
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Tutar")
        deposit_btn = QPushButton("💵 Para Yatır")
        withdraw_btn = QPushButton("💸 Para Çek")
        deposit_btn.clicked.connect(self.deposit)
        withdraw_btn.clicked.connect(self.withdraw)

        h_box = QHBoxLayout()
        h_box.addWidget(deposit_btn)
        h_box.addWidget(withdraw_btn)

        balance_btn = QPushButton("📊 Bakiye Sorgula")
        interest_btn = QPushButton("📈 Faiz Uygula (%1)")
        list_btn = QPushButton("📋 Tüm Hesapları Listele")
        update_pw_btn = QPushButton("🔑 Şifre Güncelle")
        delete_btn = QPushButton("🗑️ Hesabı Sil")
        logout_btn = QPushButton("🚪 Çıkış Yap")

        balance_btn.clicked.connect(self.check_balance)
        interest_btn.clicked.connect(self.apply_interest)
        list_btn.clicked.connect(self.show_accounts)
        update_pw_btn.clicked.connect(self.update_password)
        delete_btn.clicked.connect(self.delete_account)
        logout_btn.clicked.connect(self.logout)

        layout.addWidget(self.amount_input)
        layout.addLayout(h_box)
        layout.addWidget(balance_btn)
        layout.addWidget(interest_btn)
        layout.addWidget(list_btn)
        layout.addWidget(update_pw_btn)
        layout.addWidget(delete_btn)
        layout.addWidget(logout_btn)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def deposit(self):
        try:
            amt = float(self.amount_input.text())
            self.bank.deposit(self.account_number, amt, self.password)
            QMessageBox.information(self, "Başarılı", "Para yatırıldı.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def withdraw(self):
        try:
            amt = float(self.amount_input.text())
            self.bank.withdraw(self.account_number, amt, self.password)
            QMessageBox.information(self, "Başarılı", "Para çekildi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def check_balance(self):
        try:
            balance = self.bank.check_balance(self.account_number, self.password)
            QMessageBox.information(self, "Bakiye", f"Mevcut Bakiye: {balance:.2f} TL")
        except Exception as e:
            QMessageBox.critical(self, "Hata", str(e))

    def apply_interest(self):
        self.bank.apply_interest_to_all()
        QMessageBox.information(self, "Faiz", "Tüm hesaplara %1 faiz uygulandı.")

    def show_accounts(self):
        df = self.bank.list_accounts()
        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns)
        for row in range(len(df)):
            for col in range(len(df.columns)):
                self.table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

    def update_password(self):
        old_pw, ok1 = QInputDialog.getText(self, "Eski Şifre", "Eski şifrenizi girin:", QLineEdit.Password)
        if ok1:
            new_pw, ok2 = QInputDialog.getText(self, "Yeni Şifre", "Yeni şifrenizi girin:", QLineEdit.Password)
            if ok2:
                try:
                    self.bank.update_password(self.account_number, old_pw, new_pw)
                    self.password = new_pw
                    QMessageBox.information(self, "Başarılı", "Şifre güncellendi.")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", str(e))

    def delete_account(self):
        reply = QMessageBox.question(self, "Hesap Sil", "Hesabınızı silmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.bank.delete_account(self.account_number, self.password)
                QMessageBox.information(self, "Silindi", "Hesap silindi.")
                self.logout()
            except Exception as e:
                QMessageBox.critical(self, "Hata", str(e))

    def logout(self):
        self.close()
        self.login = LoginWindow()
        self.login.show()

# =============================================================
#                          UYGULAMA GİRİŞİ
# =============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
