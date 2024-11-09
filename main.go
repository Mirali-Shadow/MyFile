package main

import (
    "fmt"
    "log"
    "net/http"
    "os"

    tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api"
)

const (
    botToken   = "6414679474:AAHBrTFt5sCbbudkXHu3JvPrR_Pj50T30qs"
    adminID    = 7191775208 // آی‌دی عددی ادمین
)

var requiredChannels = []string{"@MIRALI_VIBE", "@shadow_R3"}

// تابع بررسی عضویت در کانال‌ها
func checkUserMembership(userID int, bot *tgbotapi.BotAPI) bool {
    for _, channel := range requiredChannels {
        chatMember, err := bot.GetChatMember(tgbotapi.ChatConfigWithUser{
            ChatID:     channel,
            UserID:     userID,
        })
        if err != nil || (chatMember.Status != "member" && chatMember.Status != "administrator" && chatMember.Status != "creator") {
            return false
        }
    }
    return true
}

func main() {
    bot, err := tgbotapi.NewBotAPI(botToken)
    if err != nil {
        log.Panic(err)
    }

    u := tgbotapi.NewUpdate(0)
    u.Timeout = 60
    updates, _ := bot.GetUpdatesChan(u)

    for update := range updates {
        if update.Message == nil {
            continue
        }

        chatID := update.Message.Chat.ID
        userID := update.Message.From.ID

        if update.Message.Text == "/start" {
            bot.Send(tgbotapi.NewMessage(adminID, fmt.Sprintf("کاربر جدید با آیدی %d ربات را استارت کرده است.", userID)))
            isMember := checkUserMembership(userID, bot)
            if !isMember {
                bot.Send(tgbotapi.NewMessage(chatID, "لطفاً ابتدا در کانال‌های موردنظر عضو شوید."))
                continue
            }
            bot.Send(tgbotapi.NewMessage(chatID, "خوش آمدید! لینک کاستوم خود را ارسال کنید."))
        }

        if update.Message.Text != "/start" && len(update.Message.Text) > 4 && update.Message.Text[:4] == "http" {
            isMember := checkUserMembership(userID, bot)
            if !isMember {
                bot.Send(tgbotapi.NewMessage(chatID, "لطفاً ابتدا در کانال‌های موردنظر عضو شوید."))
                continue
            }
            bot.Send(tgbotapi.NewDocumentUpload(chatID, "path/to/your/file1.pdf"))
            bot.Send(tgbotapi.NewDocumentUpload(chatID, "path/to/your/file2.zip"))
        }
    }
}
