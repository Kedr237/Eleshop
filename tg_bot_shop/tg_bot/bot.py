from utils import *
from telegram import Update
from telegram import CallbackQuery
from telegram import InputMediaPhoto
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder
from telegram.ext import ContextTypes
from telegram.ext import filters
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from asgiref.sync import sync_to_async
from typing import List
from users.models import Profile
from users.models import Orders
from shop.models import Category
from shop.models import Product
from shop.models import ProductImages
from config import *


# Secondary functions
async def create_profile(user_id: int, user_name: str) -> None:
  profile_exists: bool = await sync_to_async(
      Profile.objects.filter(user_id=user_id).exists
    )()
  if not profile_exists:
    await sync_to_async(Profile.objects.create)(
      user_id=user_id,
      user_name=user_name,
    )

async def update_profile_name(user_id: int, user_name: str) -> None:
  profile: Profile = await sync_to_async(Profile.objects.get)(user_id=user_id)
  if profile.user_name != user_name:
    profile.user_name = user_name
    await sync_to_async(profile.save)()

async def create_order(user_model: Profile, product_model: Product) -> None:
  await sync_to_async(Orders.objects.create)(
    user_model=user_model,
    product=product_model,
  )


def get_id_form_cb(query: CallbackQuery) -> int:
  return int(query.data.split(':')[-1])

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  categories: List[Category] = await get_objs_all(Category)
  if categories:
    reply_markup: InlineKeyboardMarkup = categories_markup(categories)
    message_text: str = 'Вот список категорий:'
    await update.message.reply_text(message_text, reply_markup=reply_markup)
  else:
    await update.message.reply_text('Категорий нет')

async def show_orders_by_status(query: CallbackQuery, user: Profile, status: str) -> None:
  order_models: List[Orders] = await get_objs_by_filter(Orders, {'user_model': user, 'order_status': status})
  start_mes: Dict[str, str] = {
    'waiting': 'Заказы ожидающие обработки:',
    'at_work': 'Заказы в работе:',
    'completed': 'Завершенные заказы:',
  }
  if order_models:
    orders: List[Dict[str, str]] = [
      {
        'prod': await sync_to_async(lambda: order.product.product_name)(),
        'date': await sync_to_async(lambda: order.date)(),
      }
      for order in order_models
    ]
    message: str = start_mes[status] + '\n' + \
      '\n'.join([f"{order['prod']} (от {order['date'].date().strftime('%d.%m.%Y')})" for order in orders])
    await query.message.reply_text(message)
  else:
    await query.message.reply_text('Здесь пусто')

async def show_del_orders(query: CallbackQuery, user_model: Profile) -> None:
  order_models: List[Orders] = await get_objs_by_filter(Orders, {'user_model': user_model})
  if order_models:
    reply_markup = await del_orders_markup(order_models)
    await query.message.reply_text('Выберите заказ, который хотите отменить:', reply_markup=reply_markup)
  else:
    await query.message.reply_text('Здесь пусто')


# Markup
def menu_markup() -> ReplyKeyboardMarkup:
  keyboard: List[List[str]] = [
    ['Категории'],
    ['Список заказов'],
  ]
  return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def categories_markup(categories: List[Category]) -> InlineKeyboardMarkup:
  keyboard: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(
      category.category_name,
      callback_data=str(f'Category:{category.id}'),
    )] for category in categories
  ]
  return InlineKeyboardMarkup(keyboard)

def products_markup(products: List[Product]) -> InlineKeyboardMarkup:
  keyboard: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(
      product.product_name,
      callback_data=str(f'Product:{product.id}')
    )] for product in products 
  ]
  return InlineKeyboardMarkup(keyboard)

def buy_markup(product: Product) -> InlineKeyboardMarkup:
  keyboard: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(
      f'Заказать',
      callback_data=str(f'Buy:{product.id}')
    )]
  ]
  return InlineKeyboardMarkup(keyboard)

def orders_markup() -> InlineKeyboardMarkup:
  buttons: List[List[str, str]] = [
    ['Заказы ожидающие обработки', 'Orders:waiting'],
    ['Заказы в работе', 'Orders:at_work'],
    ['Завершенные заказы', 'Orders:completed'],
    ['Отменить заказ', 'Orders:cancel'],
  ]
  keyboard: List[List[InlineKeyboardButton]] = [
    [InlineKeyboardButton(button[0], callback_data=button[1])]
    for button in buttons
  ]
  return InlineKeyboardMarkup(keyboard)

async def del_orders_markup(order_models: List[Orders]) -> InlineKeyboardMarkup:
  keyboard: List[List[InlineKeyboardButton]] = []
  for order in order_models:
    prod = await sync_to_async(lambda: order.product.product_name)()
    date = await sync_to_async(lambda: order.date.strftime('%d.%m.%Y'))()
    keyboard.append([InlineKeyboardButton(
        f"{prod} (от {date})",
        callback_data=f"Del_order:{prod}:{order.id}"
    )])
  return InlineKeyboardMarkup(keyboard)


# Commands
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id: int = update.effective_user.id
  user_name: str = update.effective_user.name
  await create_profile(user_id, user_name)
  await update.message.reply_text(f'Добро пожаловать', reply_markup=menu_markup())
  await show_categories(update, context)

async def categories_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await show_categories(update, context)

async def orders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text('Что вы хотите узнать?', reply_markup=orders_markup())


# Callbacks
async def category_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query: CallbackQuery = update.callback_query
  category_id: int = get_id_form_cb(query)
  category: Category = await get_obj_by_id(Category, category_id)
  products: List[Product] = await get_objs_by_filter(Product, {'product_category': category})
  reply_markup: InlineKeyboardMarkup = products_markup(products)

  message_text: str = \
  f'''
*{category.category_name}*
{category.category_desc}
  '''

  await query.answer()
  await query.message.reply_text(message_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def product_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query: CallbackQuery = update.callback_query
  product_id: int = get_id_form_cb(query)
  product: Product = await get_obj_by_id(Product, product_id)
  reply_markup: InlineKeyboardMarkup = buy_markup(product)
  media: List[InputMediaPhoto] = await get_media_photos(ProductImages, 'product', product)

  message_text: str = \
  f'''
*{product.product_name}*
*Цена: {product.product_price}*
{product.product_desc}
  '''
  message_buy: str = f'Вы можете добавить товар в список заказов.'

  await query.answer()
  if media:
    await query.message.reply_media_group(
      media=media,
      caption=message_text,
      parse_mode=ParseMode.MARKDOWN
    )
  else:
    await query.message.reply_text(message_text, parse_mode=ParseMode.MARKDOWN)
  await query.message.reply_text(message_buy, reply_markup=reply_markup)

async def buy_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id: int = update.effective_user.id
  user_name: str = update.effective_user.name
  await update_profile_name(user_id, user_name)

  query: CallbackQuery = update.callback_query
  product_id: int = get_id_form_cb(query)

  user_model: Profile = await sync_to_async(Profile.objects.get)(user_id=user_id)
  product_model: Product = await get_obj_by_id(Product, product_id)
  await create_order(user_model, product_model)

  message_text: str = \
    f'''
Вы успешно оформили заказ.
Наш представитель свяжется с вами позже.
    '''
  await query.answer()
  await query.message.reply_text(message_text)

async def orders_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  user_id: int = update.effective_user.id
  user_model: Profile = await sync_to_async(Profile.objects.get)(user_id=user_id)
  query: CallbackQuery = update.callback_query
  action: str = query.data.split(':')[-1]
  
  await query.answer()
  if action == 'cancel':
    await show_del_orders(query, user_model)
  else:
    await show_orders_by_status(query, user_model, action)

async def del_order_cb(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  query: CallbackQuery = update.callback_query
  prod_name: str = query.data.split(':')[-2]
  prod_id: str = query.data.split(':')[-1]
  order = await get_obj_by_id(Orders, prod_id)

  await query.answer()
  await sync_to_async(order.delete)()
  await query.message.reply_text(f'Заказ: "{prod_name}" успешно удален.')


# App setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handlers([
  CommandHandler('start', start_cmd),
  CommandHandler('categories', categories_cmd),
  CommandHandler('orders', orders_cmd),
  MessageHandler(filters.Regex('^Категории'), categories_cmd),
  MessageHandler(filters.Regex('^Список заказов'), orders_cmd),
  CallbackQueryHandler(callback=category_cb, pattern='^Category:'),
  CallbackQueryHandler(callback=product_cb, pattern='^Product:'),
  CallbackQueryHandler(callback=buy_cb, pattern='^Buy:'),
  CallbackQueryHandler(callback=orders_cb, pattern='^Orders:'),
  CallbackQueryHandler(callback=del_order_cb, pattern='^Del_order:'),
])

if __name__ == '__main__':
  app.run_polling(timeout=30)