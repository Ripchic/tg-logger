from tg_logger import TelegramBot
from keras_example import keras_example
from DE_example import differential_evolution
from telebot import types
import os

token = os.getenv('TOKEN')

bot = TelegramBot(token, None).bot

differential_evolution_answers = {}


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    bot.send_message(message.chat.id, text=f"Hey, {user.first_name}! 👋\n\nI'm your personal assistant📕 for logging "
                                           f"models📝, so let's get started!\n\nFirst of all, you should find out "
                                           f"your /chat_id, which you will specify in the Python🐍 project, "
                                           f"and then you can run the models using the /running_keras_example or "
                                           f"/running_the_differential_evolution commands.\n\nIf anything, call for "
                                           f"/help, and I will immediately rush to your rescue! ⛑")


@bot.message_handler(commands=['chat_id'])
def chat_id(message):
    bot.send_message(message.chat.id, f"⬇️ Your ID:")
    bot.send_message(message.chat.id, f"{message.chat.id}")


@bot.message_handler(commands=['running_keras_example'])
def running_the_keras_example_model(message):
    message_parameter = bot.send_message(message.chat.id, "Just a second... Please specify the number of epochs")
    bot.register_next_step_handler(message_parameter, processing_the_keras_example_model)


def processing_the_keras_example_model(message, flag=0):
    try:
        epochs = int(message.text)
        if epochs <= 0:
            raise ValueError
        bot.send_message(message.chat.id, f"<i>~Starting model training...</i>", parse_mode='HTML')
        keras_example(token=token, user_id=os.getenv('CHAT_ID'), n_epochs=epochs)
    except ValueError:
        flag += 1
        if flag >= 2:
            bot.send_message(message.chat.id, f"❗️<b>Failure</b>: the launch of the model has been canceled",
                             parse_mode='HTML')
        else:
            message_repeat_parameter = bot.send_message(message.chat.id, "No, no, you have to specify a natural "
                                                                         "number. Try again!")
            bot.register_next_step_handler(message_repeat_parameter,
                                           lambda msg: processing_the_keras_example_model(msg, flag + 1))


@bot.message_handler(commands=['running_the_differential_evolution'])
def running_the_differential_evolution_model(message):
    differential_evolution_answers.clear()
    markup = types.InlineKeyboardMarkup(row_width=3)
    button1 = types.InlineKeyboardButton("Rosenbrock", callback_data="Rosenbrock")
    button2 = types.InlineKeyboardButton("Rastrigin", callback_data="Rastrigin")
    button3 = types.InlineKeyboardButton("Griewank", callback_data="Griewank")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, "A good choice! Let's figure out the parameters:\n\n"
                                      "1️⃣ Specify the mathematical function", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["Rosenbrock", "Rastrigin", "Griewank"])
def running_the_differential_evolution_model_answer(call):
    bot.send_message(call.message.chat.id, call.data)
    differential_evolution_answers["fobj"] = call.data
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    message_parameter = bot.send_message(call.message.chat.id, "2️⃣ Set boundaries, for example 2")
    bot.register_next_step_handler(message_parameter, processing_the_differential_evolution_model_bounds)


def processing_the_differential_evolution_model_bounds(message, flag=0):
    try:
        bounds = int(message.text)
        if bounds <= 0:
            raise ValueError
        differential_evolution_answers["bounds"] = [[-bounds, bounds], [-bounds, bounds]]
        message_parameter = bot.send_message(message.chat.id, "3️⃣ The mutation coefficient. The value in the range "
                                                              "from 0 to 1, for example 0.3")
        bot.register_next_step_handler(message_parameter,
                                       processing_the_differential_evolution_model_mutation_coefficient)
    except ValueError:
        flag += 1
        if flag >= 2:
            bot.send_message(message.chat.id, f"❗️<b>Failure</b>: the launch of the model has been canceled",
                             parse_mode='HTML')
            differential_evolution_answers.clear()
        else:
            message_repeat_parameter = bot.send_message(message.chat.id, "No, no, you have to specify a natural "
                                                                         "number. Try again!")
            bot.register_next_step_handler(message_repeat_parameter,
                                           lambda msg: processing_the_differential_evolution_model_bounds(msg,
                                                                                                          flag + 1))


def processing_the_differential_evolution_model_mutation_coefficient(message, flag=0):
    try:
        mutation_coefficient = float(message.text)
        if mutation_coefficient <= 0 or mutation_coefficient >= 1:
            raise ValueError
        differential_evolution_answers["mutation_coefficient"] = mutation_coefficient
        message_parameter = bot.send_message(message.chat.id, "4️⃣ The crossover coefficient. The value in the range "
                                                              "from 0 to 1, for example 0.5")
        bot.register_next_step_handler(message_parameter,
                                       processing_the_differential_evolution_model_crossover_coefficient)
    except ValueError:
        flag += 1
        if flag >= 2:
            bot.send_message(message.chat.id, f"❗️<b>Failure</b>: the launch of the model has been canceled",
                             parse_mode='HTML')
            differential_evolution_answers.clear()
        else:
            message_repeat_parameter = bot.send_message(message.chat.id, "Nope, it should be a number in the range "
                                                                         "from 0 to 1. Try again!")
            bot.register_next_step_handler(message_repeat_parameter,
                                           lambda msg: processing_the_differential_evolution_model_mutation_coefficient(
                                               msg, flag + 1))


def processing_the_differential_evolution_model_crossover_coefficient(message, flag=0):
    try:
        crossover_coefficient = float(message.text)
        if crossover_coefficient <= 0 or crossover_coefficient >= 1:
            raise ValueError
        differential_evolution_answers["crossover_coefficient"] = crossover_coefficient
        message_parameter = bot.send_message(message.chat.id,
                                             "5️⃣ Population size, for example 500")
        bot.register_next_step_handler(message_parameter,
                                       processing_the_differential_evolution_model_population_size)
    except ValueError:
        flag += 1
        if flag >= 2:
            bot.send_message(message.chat.id, f"❗️<b>Failure</b>: the launch of the model has been canceled",
                             parse_mode='HTML')
            differential_evolution_answers.clear()
        else:
            message_repeat_parameter = bot.send_message(message.chat.id, "Nope, it should be a number in the range "
                                                                         "from 0 to 1. Try again!")
            bot.register_next_step_handler(message_repeat_parameter,
                                           lambda
                                               msg: processing_the_differential_evolution_model_crossover_coefficient(
                                               msg, flag + 1))


def processing_the_differential_evolution_model_population_size(message, flag=0):
    try:
        population_size = int(message.text)
        if population_size <= 0:
            raise ValueError
        differential_evolution_answers["population_size"] = population_size
        message_parameter = bot.send_message(message.chat.id,
                                             "6️⃣ Iterations, for example 50")
        bot.register_next_step_handler(message_parameter,
                                       processing_the_differential_evolution_model_iterations)
    except ValueError:
        flag += 1
        if flag >= 2:
            bot.send_message(message.chat.id, f"❗️<b>Failure</b>: the launch of the model has been canceled",
                             parse_mode='HTML')
            differential_evolution_answers.clear()
        else:
            message_repeat_parameter = bot.send_message(message.chat.id, "No, no, you have to specify a natural "
                                                                         "number. Try again!")
            bot.register_next_step_handler(message_repeat_parameter,
                                           lambda msg: processing_the_differential_evolution_model_population_size(msg,
                                                                                                                   flag + 1))


def processing_the_differential_evolution_model_iterations(message, flag=0):
    try:
        iterations = int(message.text)
        if iterations <= 0:
            raise ValueError
        differential_evolution_answers["iterations"] = iterations
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("LatinHypercube", callback_data="LatinHypercube")
        button2 = types.InlineKeyboardButton("Halton", callback_data="Halton")
        button3 = types.InlineKeyboardButton("Sobol", callback_data="Sobol")
        button4 = types.InlineKeyboardButton("Random", callback_data="Random")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, "7️⃣ Statistical method", reply_markup=markup)
    except ValueError:
        flag += 1
        if flag >= 2:
            bot.send_message(message.chat.id, f"❗️<b>Failure</b>: the launch of the model has been canceled",
                             parse_mode='HTML')
            differential_evolution_answers.clear()
        else:
            message_repeat_parameter = bot.send_message(message.chat.id, "No, no, you have to specify a natural "
                                                                         "number. Try again!")
            bot.register_next_step_handler(message_repeat_parameter,
                                           lambda msg: processing_the_differential_evolution_model_iterations(msg,
                                                                                                              flag + 1))


@bot.callback_query_handler(func=lambda call: call.data in ["LatinHypercube", "Halton", "Sobol", "Random"])
def processing_the_differential_evolution_model_statistical_method_answer(call):
    bot.send_message(call.message.chat.id, call.data)
    differential_evolution_answers["init_setting"] = call.data
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("rand2", callback_data="rand2")
    button2 = types.InlineKeyboardButton("best1", callback_data="best1")
    button3 = types.InlineKeyboardButton("rand_to_p_best1", callback_data="rand_to_p_best1")
    markup.add(button1, button2, button3)
    bot.send_message(call.message.chat.id, "8️⃣ Mutation settings", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["rand2", "best1", "rand_to_p_best1"])
def processing_the_differential_evolution_model_mutation_settings_answer(call):
    bot.send_message(call.message.chat.id, call.data)
    differential_evolution_answers["mutation_setting"] = call.data
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    markup = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton("worst", callback_data="worst")
    button2 = types.InlineKeyboardButton("random_among_worst", callback_data="random_among_worst")
    button3 = types.InlineKeyboardButton("random_selection", callback_data="random_selection")
    markup.add(button1, button2, button3)
    bot.send_message(call.message.chat.id, "9️⃣ Selection settings", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ["worst", "random_among_worst", "random_selection"])
def processing_the_differential_evolution_model_selection_settings_answer(call):
    bot.send_message(call.message.chat.id, call.data)
    differential_evolution_answers["selection_setting"] = call.data
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, f"<i>~Starting model training...</i>", parse_mode='HTML')
    differential_evolution(get_token=token,
                           get_chat_id=os.getenv('CHAT_ID'),
                           fobj=differential_evolution_answers["fobj"],
                           bounds=differential_evolution_answers["bounds"],
                           mutation_coefficient=differential_evolution_answers["mutation_coefficient"],
                           crossover_coefficient=differential_evolution_answers["crossover_coefficient"],
                           population_size=differential_evolution_answers["population_size"],
                           iterations=differential_evolution_answers["iterations"],
                           init_setting=differential_evolution_answers["init_setting"],
                           mutation_setting=differential_evolution_answers["mutation_setting"],
                           selection_setting=differential_evolution_answers["selection_setting"])


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"Of course! Here is a list of possible commands:\n\n"
                                      f"/start — Getting started\n\n"
                                      f"/chat_id — Find out your Chat ID\n\n"
                                      f"/running_keras_example — Launch the Keras model\n\n"
                                      f"/running_the_differential_evolution — Launch the Differential Evolution "
                                      f"model\n\n"
                                      f"/help — Help")


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, f"I don't understand... But maybe you will be satisfied that the 🅰️nswer to the "
                                      f"Main question of Life, the Universe and everything else is 42! 🪐 ✨\n\nIf "
                                      f"that's not enough, use /help 🛟")


bot.polling()
