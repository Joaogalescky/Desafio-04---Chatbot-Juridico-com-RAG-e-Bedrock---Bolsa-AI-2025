from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from chatbot.ingestion import download_from_s3, load_and_split
from chatbot.vectorstore import build_vector_store
from chatbot.chain import get_qa_chain
from chatbot.config import TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Sou o Chatbot Jurídico \nDigite sua pergunta ou use /atualizar para carregar a base")


async def atualizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Atualizando a base de dados...")
    try:
        download_from_s3()
        docs = load_and_split()
        if not docs:
            await update.message.reply_text("Não foi possível atualizar a base de dados")
        else:
            build_vector_store(docs)
            await update.message.reply_text("Base de dados atualizada com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"Erro ao atualizar a base de dados: {e}")


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = update.message.text
    await update.message.reply_text(f"Recebi sua pergunta: {pergunta}" + "\nProcessando sua pergunta...")
    try:
        resposta = get_qa_chain(pergunta)
        texto = resposta.get("aswer", "Não consegui gerar uma resposta")
        await update.message.reply_text(f"{texto}")
    except Exception as e:
        await update.message.reply_text(f"Erro ao processar sua pergunta: {e}")
        
        
def main():
    if not TOKEN:
        raise ValueError("⚠️ Variável de ambiente TELEGRAM_TOKEN não configurada!")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("atualizar", atualizar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()

# Para rodar o bot no Telegram, use:
    # t.me/chatbot_juridico_bot
    # Token: 8304485718:AAFeqEuONC6pR8lsNsHZvcGYX5UVMoGk9P4
    # Na pasta raiz do projeto, execute: pip install python-telegram-bot==20.3
    # Depois, execute: set TELEGRAM_TOKEN=8304485718:AAFeqEuONC6pR8lsNsHZvcGYX5UVMoGk9P4
    # Depois, execute: python app/bot.py