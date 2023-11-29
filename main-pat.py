from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
import random

key_token = ""  # Masukkan KEY-TOKEN BOT
user_bot = ""  # Masukkan @user bot

# Variable to store the secret number for the number guessing game
secret_number = None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_list = [
        "/start - Memulai bot",
        "/help - Menampilkan bantuan",
        "/startgame - Memulai permainan tebak angka",
        "/startwordgame - Memulai permainan tebak kata",
        # Tambahkan command mini-games lainnya jika ada
    ]
    command_text = "\n".join(command_list)
    await update.message.reply_text(f"Gunakan /help untuk menampilkan apa yang dapat saya berikan..\n\nCommand yang tersedia:\n{command_text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim pesan, bot akan membalas pesan..")

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_received: str = update.message.text
    print(f"Pesan diterima: {text_received}")
    text_lower_received = text_received.lower()
    
    # Check if the received message is numeric
    if text_received.isdigit():
        # Handle numeric input (e.g., for games)
        await handle_numeric_input(int(text_received), update)
    else:
        if 'halo' in text_lower_received:
            await update.message.reply_text("Hallo juga")
        elif 'selamat malam' in text_lower_received:
            await update.message.reply_text("Selamat malam..., jangan lupa istirahat 😊")
        elif 'siapa kamu ?' in text_lower_received:
            await update.message.reply_text(f"Bot adalah: {user_bot}")
        else:
            await update.message.reply_text("Bot tidak mengerti")

# Function to handle numeric input (e.g., for games)
async def handle_numeric_input(number: int, update: Update):
    global secret_number
    
    if secret_number is not None:
        # Check if the guessed number is correct
        if number == secret_number:
            await update.message.reply_text("Selamat! Anda menebak angka dengan benar.")
            # Reset the secret number after the game is finished
            secret_number = None
        else:
            await update.message.reply_text("Maaf, tebakan Anda salah. Coba lagi!")
    else:
        await update.message.reply_text("Maaf, tidak ada permainan tebak angka yang sedang berlangsung.")

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global secret_number
    # Set a new secret number for the game
    secret_number = random.randint(1, 100)
    await update.message.reply_text("Ayo tebak angka antara 1 dan 100!")

# Definisi dictionary untuk menyimpan status permainan tebak kata
word_game_status = {}

async def start_word_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global word_game_status

    # Cek apakah sudah ada permainan tebak kata yang sedang berlangsung
    if update.message.chat_id in word_game_status:
        await update.message.reply_text("Maaf, permainan tebak kata sudah berlangsung. Selesaikan terlebih dahulu.")
        return

    # Logika untuk permainan tebak kata
    word_list = ['python', 'telegram', 'bot', 'coding', 'challenge']
    secret_word = random.choice(word_list)
    hint = ['_'] * len(secret_word)

    # Simpan status permainan ke dalam dictionary
    word_game_status[update.message.chat_id] = {'secret_word': secret_word, 'hint': hint}

    await update.message.reply_text(f"Ayo tebak kata: {' '.join(hint)}")
    await update.message.reply_text("Kirim satu huruf untuk menebak kata!")

async def guess_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global word_game_status

    # Cek apakah ada permainan tebak kata yang sedang berlangsung
    if update.message.chat_id not in word_game_status:
        await update.message.reply_text("Tidak ada permainan tebak kata yang sedang berlangsung.")
        return

    # Ambil huruf yang dikirim pengguna
    guessed_letter = update.message.text.lower()

    # Cek apakah huruf yang dikirim adalah huruf tunggal
    if len(guessed_letter) != 1 or not guessed_letter.isalpha():
        await update.message.reply_text("Kirim satu huruf untuk menebak kata!")
        return

    # Ambil status permainan dari dictionary
    game_data = word_game_status[update.message.chat_id]
    secret_word = game_data['secret_word']
    hint = game_data['hint']

    # Cek apakah huruf yang ditebak benar
    if guessed_letter in secret_word:
        # Perbarui petunjuk dengan huruf yang benar
        for i in range(len(secret_word)):
            if secret_word[i] == guessed_letter:
                hint[i] = guessed_letter

        # Cek apakah sudah berhasil menebak seluruh kata
        if '_' not in hint:
            del word_game_status[update.message.chat_id]  # Hapus status permainan
            await update.message.reply_text(f"Selamat! Anda berhasil menebak kata: {' '.join(hint)}")
            return

        # Perbarui status permainan
        word_game_status[update.message.chat_id]['hint'] = hint
        await update.message.reply_text(f"Benar! Kata sekarang: {' '.join(hint)}")
    else:
        await update.message.reply_text("Salah! Coba lagi.")

# ...

# Tambahkan handler untuk menerima tebakan huruf
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guess_word))

# ...

# Update fungsi text_message untuk menangani input teks
async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_received: str = update.message.text
    print(f"Pesan diterima: {text_received}")
    text_lower_received = text_received.lower()

    # Cek apakah pengguna sedang bermain tebak kata
    if update.message.chat_id in word_game_status:
        await guess_word(update, context)  # Panggil fungsi untuk menebak huruf
    else:
        # Fungsi text_message yang sudah ada
        if 'halo' in text_lower_received:
            await update.message.reply_text("Hallo juga")
        elif 'selamat malam' in text_lower_received:
            await update.message.reply_text("Selamat malam..., jangan lupa istirahat 😊")
        elif 'siapa kamu ?' in text_lower_received:
            await update.message.reply_text(f"Bot adalah: {user_bot}")
        else:
            await update.message.reply_text("Bot tidak mengerti")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")

if __name__ == '__main__':
    print("Mulai")
    app = Application.builder().token(key_token).build()
    # COMMAND :
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('startgame', start_game))
    app.add_handler(CommandHandler('startwordgame', start_word_game))
    # MESSAGE:
    app.add_handler(MessageHandler(filters.TEXT, text_message))
    # error :
    app.add_error_handler(error)
    # polling :
    app.run_polling(poll_interval=1)
