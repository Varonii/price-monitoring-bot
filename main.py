import os
import random
import asyncio
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import banco
from preco import pegar_produto

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

load_dotenv("token.env")
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu monitoro preços na Amazon.\n\n"
        "/adicionar <link> - começar a monitorar um produto\n"
        "/listar - ver seus produtos\n"
        "/remover <id> - parar de monitorar"
    )

async def adicionar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use assim: /adicionar <link do produto na Amazon>")
        return

    url = context.args[0]
    if "amazon.com.br" not in url:
        await update.message.reply_text("Por enquanto só aceito links da Amazon (amazon.com.br).")
        return

    await update.message.reply_text("Buscando o produto...")
    try:
        titulo, preco = await asyncio.to_thread(pegar_produto, url)
    except Exception:
        await update.message.reply_text("Não consegui acessar esse link. Confira se está correto.")
        return

    if not titulo or preco is None:
        await update.message.reply_text("Não consegui ler o nome ou o preço desse produto.")
        return

    chat_id = update.effective_chat.id
    if banco.adicionar_produto(chat_id, url, titulo, preco):
        await update.message.reply_text(f"Adicionado!\n{titulo}\nPreço atual: R$ {preco:.2f}")
    else:
        await update.message.reply_text("Você já está monitorando esse produto.")

async def listar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produtos = banco.listar_produtos(update.effective_chat.id)
    if not produtos:
        await update.message.reply_text("Você ainda não está monitorando nenhum produto.")
        return

    linhas = []
    for produto_id, titulo, preco, url in produtos:
        linhas.append(f"[{produto_id}] {titulo[:60]}\nR$ {preco:.2f}")
    await update.message.reply_text("\n\n".join(linhas))

async def remover(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Use assim: /remover <id> (veja o id com /listar)")
        return

    produto_id = int(context.args[0])
    if banco.remover_produto(update.effective_chat.id, produto_id):
        await update.message.reply_text("Produto removido.")
    else:
        await update.message.reply_text("Não encontrei um produto seu com esse id.")

async def checar_precos(context: ContextTypes.DEFAULT_TYPE):
    logging.info("Checando preços...")
    for produto_id, chat_id, url, titulo, ultimo_preco in banco.listar_todos():
        try:
            _, novo_preco = await asyncio.to_thread(pegar_produto, url)
        except Exception as erro:
            logging.warning(f"Falha ao checar {url}: {erro}")
            continue

        if novo_preco is None:
            continue

        if ultimo_preco is not None and novo_preco < ultimo_preco:
            await context.bot.send_message(
                chat_id=chat_id,
                text=(
                    f"📉 O preço caiu!\n\n{titulo}\n"
                    f"De R$ {ultimo_preco:.2f} por R$ {novo_preco:.2f}\n\n{url}"
                ),
            )

        if novo_preco != ultimo_preco:
            banco.atualizar_preco(produto_id, novo_preco)

        await asyncio.sleep(random.uniform(5, 10))

banco.criar_tabelas()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("adicionar", adicionar))
app.add_handler(CommandHandler("listar", listar))
app.add_handler(CommandHandler("remover", remover))
app.job_queue.run_repeating(checar_precos, interval=6 * 60 * 60, first=60)
app.run_polling()