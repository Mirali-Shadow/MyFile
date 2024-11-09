package main

import (
	"fmt"
	"log"
	"os"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
)

var fileLinks = map[string]string{
	"file2": "https://github.com/Mirali-Shadow/MyFile/raw/refs/heads/main/music/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3",
	"file3": "https://www.example.com/file3.pdf",
}

func main() {
	// توکن ربات تلگرام شما
	token := "6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40"

	// اتصال به API تلگرام
	bot, err := tgbotapi.NewBotAPI(token)
	if err != nil {
		log.Panic(err)
	}

	// راه‌اندازی آپدیت‌ها
	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates, err := bot.GetUpdatesChan(u)

	// پردازش آپدیت‌ها
	for update := range updates {
		if update.Message == nil {
			continue
		}

		// شناسه چت کاربر
		chatID := update.Message.Chat.ID

		// متن پیام کاربر
		text := update.Message.Text

		// بررسی اینکه آیا پیام شامل start=... است
		if len(text) > 6 && text[:6] == "start=" {
			command := text[6:] // پارامتر بعد از "start="

			// بررسی و ارسال فایل
			if fileURL, exists := fileLinks[command]; exists {
				// ارسال فایل به کاربر
				file := tgbotapi.NewDocumentUpload(chatID, fileURL)
				_, err := bot.Send(file)
				if err != nil {
					log.Printf("Error sending file: %v", err)
				}
			} else {
				// ارسال پیام خطا در صورت عدم وجود فایل
				msg := tgbotapi.NewMessage(chatID, "لینک نامعتبر است.")
				bot.Send(msg)
			}
		} else {
			// اگر پارامتر start= وجود ندارد
			msg := tgbotapi.NewMessage(chatID, "لطفا لینک معتبر ارسال کنید.")
			bot.Send(msg)
		}
	}
}
