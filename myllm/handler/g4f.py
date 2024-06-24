"""
🔗 G4F

"""

import importlib
from time import sleep

from loguru import logger

from .client import AIClient


class G4fHandler(AIClient):
    """
    MyLLM class for G4F

    """

    def __init__(self, **kwargs):
        """
        Initialize the MyLLM object

        Args:
            None
        """
        try:
            super().__init__(**kwargs)
            logger.debug("G4F provider initializing")
            if self.enabled:
                provider_module_name = self.llm_provider
                provider_module = importlib.import_module(provider_module_name)
                provider_class = getattr(
                    provider_module, provider_module_name.split(".")[-1]
                )
                self.provider = provider_class()
                self.client = self.provider
                logger.info("Provider {} initialized ", self.provider)
            else:
                return None
        except Exception as error:
            logger.error("G4F initialization error {}", error)
            return None

    async def chat(self, prompt):
        """
        Asynchronously chats with the user.

        Args:
            prompt (str): The prompt message from the user.

        Returns:
            str: The response from the conversation model.
        """
        try:
            self.conversation.add_message("user", prompt)

            response = await self.provider.create_async(
                model=self.llm_model,
                messages=self.conversation.get_messages(),
            )

            sleep(self.timeout)

            logger.debug("response {}", response)
            if response:
                self.conversation.add_message("assistant", response)
                formatted_response = f"{self.llm_prefix} {response}"
                logger.debug("User: {}, AI: {}", prompt, response)
                return formatted_response
        except Exception as error:
            logger.error("No response {}", error)
            return "Error with client"
