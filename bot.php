<?php

// توکن ربات تلگرام شما
$token = '6352712951:AAHtDi_d8NfcmpaYYE9uqX9jZGD-6lsyj40';

// URL API تلگرام برای ارسال پیام و فایل
$apiURL = "https://api.telegram.org/bot$token/";

// لینک‌های فایل‌ها که می‌خواهید ارسال کنید
$fileLinks = [
    'file1' => 'https://github.com/Mirali-Shadow/MyFile/blob/de8645596bf6145cec4b76d5fd07786420b1e817/music/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3',
    'file2' => 'https://github.com/Mirali-Shadow/MyFile/raw/refs/heads/main/music/Pishro%20-%20Tamum%20Shode%20(featuring%20Kamyar).mp3',
    'file3' => 'https://www.example.com/file3.pdf',
];

// دریافت اطلاعات پیام از تلگرام
$input = file_get_contents("php://input");
$data = json_decode($input, true);

// بررسی اینکه آیا داده‌های ورودی معتبر است
if (isset($data['message'])) {
    // شناسه چت کاربر
    $chatId = $data['message']['chat']['id'];

    // متن پیام ارسالی توسط کاربر
    $message = $data['message']['text'];

    // استخراج پارامتر استارت
    if (isset($message) && strpos($message, 'start=') !== false) {
        $command = explode('=', $message)[1];  // پارامتر بعد از "start="

        // بررسی و ارسال فایل
        if (isset($fileLinks[$command])) {
            // لینک فایل مورد نظر
            $fileUrl = $fileLinks[$command];
            
            // ارسال فایل به کاربر
            $url = $apiURL . "sendDocument?chat_id=$chatId&document=" . urlencode($fileUrl);
            file_get_contents($url);
        } else {
            // اگر فایل پیدا نشد
            $url = $apiURL . "sendMessage?chat_id=$chatId&text=لینک نامعتبر است.";
            file_get_contents($url);
        }
    } else {
        // اگر پارامتر start= وجود ندارد
        $url = $apiURL . "sendMessage?chat_id=$chatId&text=لطفا لینک معتبر ارسال کنید.";
        file_get_contents($url);
    }
} else {
    // اگر پیام ارسال‌شده معتبر نبود
    echo "No valid input received.";
}

?>
