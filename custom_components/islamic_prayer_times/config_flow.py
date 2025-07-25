"""Config flow for Islamic Prayer Times integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    LocationSelector,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
)

from .const import (
    CALC_METHODS,
    CONF_CALC_METHOD,
    CONF_FAJR_ANGLE,
    CONF_ISHA_ANGLE,
    CONF_LAT_ADJ_METHOD,
    CONF_MAGHRIB_ANGLE,
    CONF_MIDNIGHT_MODE,
    CONF_SCHOOL,
    DEFAULT_CALC_METHOD,
    DEFAULT_CUSTOM_ANGLE,
    DEFAULT_LAT_ADJ_METHOD,
    DEFAULT_MIDNIGHT_MODE,
    DEFAULT_SCHOOL,
    DOMAIN,
    LAT_ADJ_METHODS,
    MIDNIGHT_MODES,
    NAME,
    SCHOOLS,
)


class IslamicPrayerFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle the Islamic Prayer config flow."""

    VERSION = 1
    MINOR_VERSION = 2

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> IslamicPrayerOptionsFlowHandler:
        """Get the options flow for this handler."""
        return IslamicPrayerOptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:
            lat: float = user_input[CONF_LOCATION][CONF_LATITUDE]
            lon: float = user_input[CONF_LOCATION][CONF_LONGITUDE]
            await self.async_set_unique_id(f"{lat}-{lon}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={
                    CONF_LATITUDE: lat,
                    CONF_LONGITUDE: lon,
                },
            )

        home_location = {
            CONF_LATITUDE: self.hass.config.latitude,
            CONF_LONGITUDE: self.hass.config.longitude,
        }
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=NAME): TextSelector(),
                    vol.Required(
                        CONF_LOCATION, default=home_location
                    ): LocationSelector(),
                }
            ),
        )


class IslamicPrayerOptionsFlowHandler(OptionsFlow):
    """Handle Islamic Prayer client options."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Optional(
                CONF_CALC_METHOD,
                default=self.config_entry.options.get(
                    CONF_CALC_METHOD, DEFAULT_CALC_METHOD
                ),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=CALC_METHODS,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_CALC_METHOD,
                )
            ),
            vol.Optional(
                CONF_LAT_ADJ_METHOD,
                default=self.config_entry.options.get(
                    CONF_LAT_ADJ_METHOD, DEFAULT_LAT_ADJ_METHOD
                ),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=LAT_ADJ_METHODS,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_LAT_ADJ_METHOD,
                )
            ),
            vol.Optional(
                CONF_MIDNIGHT_MODE,
                default=self.config_entry.options.get(
                    CONF_MIDNIGHT_MODE, DEFAULT_MIDNIGHT_MODE
                ),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=MIDNIGHT_MODES,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_MIDNIGHT_MODE,
                )
            ),
            vol.Optional(
                CONF_SCHOOL,
                default=self.config_entry.options.get(CONF_SCHOOL, DEFAULT_SCHOOL),
            ): SelectSelector(
                SelectSelectorConfig(
                    options=SCHOOLS,
                    mode=SelectSelectorMode.DROPDOWN,
                    translation_key=CONF_SCHOOL,
                )
            ),
            vol.Optional(
                CONF_FAJR_ANGLE,
                default=self.config_entry.options.get(CONF_FAJR_ANGLE, DEFAULT_CUSTOM_ANGLE),
            ): NumberSelector(
                NumberSelectorConfig(
                    mode=NumberSelectorMode.BOX,
                    step="any",
                )
            ),
            vol.Optional(
                CONF_MAGHRIB_ANGLE,
                default=self.config_entry.options.get(CONF_MAGHRIB_ANGLE, DEFAULT_CUSTOM_ANGLE),
            ): NumberSelector(
                NumberSelectorConfig(
                    mode=NumberSelectorMode.BOX,
                    step="any",
                )
            ),
            vol.Optional(
                CONF_ISHA_ANGLE,
                default=self.config_entry.options.get(CONF_ISHA_ANGLE, DEFAULT_CUSTOM_ANGLE),
            ): NumberSelector(
                NumberSelectorConfig(
                    mode=NumberSelectorMode.BOX,
                    step="any",
                )
            ),
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
