"""Config flow for Islamic Prayer Times integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    CALC_METHODS,
    CONF_CALC_METHOD,
    CONF_LAT_ADJ_METHOD,
    CONF_MIDNIGHT_MODE,
    CONF_SCHOOL,
    CONF_TUNE,
    DEFAULT_CALC_METHOD,
    DEFAULT_LAT_ADJ_METHOD,
    DEFAULT_MIDNIGHT_MODE,
    DEFAULT_SCHOOL,
    DOMAIN,
    LAT_ADJ_METHODS,
    MIDNIGHT_MODES,
    NAME,
    SCHOOLS,
    TIMES_TUNE,
    CONF_FAJR_ANGLE,
    CONF_MAGHRIB_ANGLE_MINUTES,
    CONF_ISHA_ANGLE_MINUTES
)


class IslamicPrayerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the Islamic Prayer config flow."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return IslamicPrayerOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self.async_show_form(step_id="user")

        return self.async_create_entry(title=NAME, data=user_input)


class IslamicPrayerOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Islamic Prayer client options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            self.options.update(user_input)
            return await self.async_step_set_times_tune()

        options = {
            vol.Optional(
                CONF_CALC_METHOD,
                default=self.config_entry.options.get(
                    CONF_CALC_METHOD, DEFAULT_CALC_METHOD
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(options=CALC_METHODS)
            ),
            vol.Optional(
                CONF_SCHOOL,
                default=self.config_entry.options.get(CONF_SCHOOL, DEFAULT_SCHOOL),
            ): selector.SelectSelector(selector.SelectSelectorConfig(options=SCHOOLS)),
            vol.Optional(
                CONF_MIDNIGHT_MODE,
                default=self.config_entry.options.get(
                    CONF_MIDNIGHT_MODE, DEFAULT_MIDNIGHT_MODE
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(options=MIDNIGHT_MODES)
            ),
            vol.Optional(
                CONF_LAT_ADJ_METHOD,
                default=self.config_entry.options.get(
                    CONF_LAT_ADJ_METHOD, DEFAULT_LAT_ADJ_METHOD
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(options=LAT_ADJ_METHODS)
            ),
            vol.Optional(
                CONF_FAJR_ANGLE,
                default=self.config_entry.options.get(
                    CONF_FAJR_ANGLE, 0
                ),
            ): int,
            vol.Optional(
                CONF_MAGHRIB_ANGLE_MINUTES,
                default=self.config_entry.options.get(
                    CONF_MAGHRIB_ANGLE_MINUTES, 0
                ),
            ): int,
            vol.Optional(
                CONF_ISHA_ANGLE_MINUTES,
                default=self.config_entry.options.get(
                    CONF_ISHA_ANGLE_MINUTES, 0
                ),
            ): int,
        }

        return self.async_show_form(
            step_id="init", data_schema=vol.Schema(options), last_step=False
        )

    async def async_step_set_times_tune(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Set time tunes for prayer times."""
        if user_input is not None:
            self.options[CONF_TUNE] = {}
            for prayer_tune, offset in user_input.items():
                if offset != 0:
                    self.options[CONF_TUNE][prayer_tune] = offset
            return self.async_create_entry(title="", data=self.options)

        time_tune_options = self.config_entry.options.get(CONF_TUNE, {})
        form_options = {}
        for time_tune in TIMES_TUNE:
            form_options.update(
                {
                    vol.Optional(
                        time_tune,
                        default=time_tune_options.get(time_tune, 0),
                    ): vol.All(
                        selector.NumberSelector(
                            selector.NumberSelectorConfig(
                                mode=selector.NumberSelectorMode.BOX
                            )
                        ),
                        vol.Coerce(int),
                    )
                }
            )
        return self.async_show_form(
            step_id="set_times_tune",
            data_schema=vol.Schema(form_options),
            last_step=True,
        )
