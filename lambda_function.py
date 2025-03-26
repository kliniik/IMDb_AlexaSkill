# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_slot_value # para leer los slots

from ask_sdk_model import Response

from peliculas import buscarIMDb

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bienvenido a la Enciclopedia de Películas. ¡Pregúntame sobre tu película favorita!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class NotaIntentHandler(AbstractRequestHandler):
    """Handler for Nota Intent."""
    def can_handle(self, handler_input):
    # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NotaIntent")(handler_input) # nombre del intent
        
    def handle(self, handler_input):
        pelicula = get_slot_value(handler_input=handler_input, slot_name="movieTitle") # valor slot
        if not pelicula:
            return handler_input.response_builder.speak("No entendí el título de la película. ¿Puedes repetirlo?").ask("¿Puedes repetir el título?").response
        
        dict_peli = buscarIMDb(pelicula) # código externo
        
        score = dict_peli.get("Puntuación")
        pelicula = pelicula.title()
        if score:
            speak_output = f'La nota de {pelicula} es de {score} sobre 10.'
        else:
            speak_output = f'No he podido averiguar la nota de {pelicula} + . ¿Puedes preguntar de otro modo?'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("¿Quieres preguntar por otra película?")
                .response
        )

class VotosIntentHandler(AbstractRequestHandler):
    """Handler for Votos Intent."""
    def can_handle(self, handler_input):
    # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("VotosIntent")(handler_input) # nombre del intent
        
    def handle(self, handler_input):
        pelicula = get_slot_value(handler_input=handler_input, slot_name="movieTitle") # valor slot
        if not pelicula:
            return handler_input.response_builder.speak("No entendí el título de la película. ¿Puedes repetirlo?").ask("¿Puedes repetir el título?").response
            
        dict_peli = buscarIMDb(pelicula) # código externo
        
        votos = dict_peli.get("Número de votos")
        pelicula = pelicula.title()
        
        if votos:
            speak_output = f'El número de votos de {pelicula} es {votos}.'
        else:
            speak_output = f'No he podido averiguar el número de votos de {pelicula} + . ¿Puedes preguntar de otro modo?'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("¿Quieres preguntar por otra película?")
                .response
        )

class SinopsisIntentHandler(AbstractRequestHandler):
    """Handler for Sinopsis Intent."""
    def can_handle(self, handler_input):
    # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SinopsisIntent")(handler_input) # nombre del intent
        
    def handle(self, handler_input):
        pelicula = get_slot_value(handler_input=handler_input, slot_name="movieTitle") # valor slot
        if not pelicula:
            return handler_input.response_builder.speak("No entendí el título de la película. ¿Puedes repetirlo?").ask("¿Puedes repetir el título?").response
            
        dict_peli = buscarIMDb(pelicula) # código externo
        
        sinopsis = dict_peli.get("Descripción")
        pelicula = pelicula.title()
        
        if sinopsis:
            speak_output = f'La sinopsis de {pelicula} es: {sinopsis}'
        else:
            speak_output = f'No he podido averiguar la sinopsis de {pelicula} + . ¿Puedes preguntar de otro modo?'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("¿Quieres preguntar por otra película?")
                .response
        )

class DirectorIntentHandler(AbstractRequestHandler):
    """Handler for Director Intent."""
    def can_handle(self, handler_input):
    # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DirectorIntent")(handler_input) # nombre del intent
        
    def handle(self, handler_input):
        pelicula = get_slot_value(handler_input=handler_input, slot_name="movieTitle") # valor slot
        if not pelicula:
            return handler_input.response_builder.speak("No entendí el título de la película. ¿Puedes repetirlo?").ask("¿Puedes repetir el título?").response
            
        dict_peli = buscarIMDb(pelicula) # código externo
        
        director = dict_peli.get("Director")
        pelicula = pelicula.title()
        
        if director:
            speak_output = f'El director de {pelicula} es {director}.'
        else:
            speak_output = f'No he podido averiguar el director de {pelicula} + . ¿Puedes preguntar de otro modo?'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("¿Quieres preguntar por otra película?")
                .response
        )

class DurationIntentHandler(AbstractRequestHandler):
    """Handler for Duration Intent."""
    def can_handle(self, handler_input):
    # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("DurationIntent")(handler_input) # nombre del intent
        
    def handle(self, handler_input):
        pelicula = get_slot_value(handler_input=handler_input, slot_name="movieTitle") # valor slot
        if not pelicula:
            return handler_input.response_builder.speak("No entendí el título de la película. ¿Puedes repetirlo?").ask("¿Puedes repetir el título?").response
            
        dict_peli = buscarIMDb(pelicula) # código externo
        
        duration = dict_peli.get("Duración")
        pelicula = pelicula.title()
        
        if duration:
            speak_output = f'La duración de {pelicula} es {duration}.'
        else:
            speak_output = f'No he podido averiguar la duración de {pelicula} + . ¿Puedes preguntar de otro modo?'
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("¿Quieres preguntar por otra película?")
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hasta luego!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, no estoy segura. Puedes decir Hello o Help. ¿Qué quieres hacer?"
        reprompt = "No lo entendí. ¿En qué puedo ayudarte?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Lo siento, he tenido problemas para hacer lo que me pedías. Por favor, inténtelo de nuevo."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# private handlers
sb.add_request_handler(NotaIntentHandler())
sb.add_request_handler(VotosIntentHandler())
sb.add_request_handler(SinopsisIntentHandler())
sb.add_request_handler(DirectorIntentHandler())
sb.add_request_handler(DurationIntentHandler())

sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()