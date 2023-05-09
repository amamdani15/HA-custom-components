"""Platform to retrieve Islamic prayer times information for Home Assistant."""

from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, PRAYER_TIMES_ICON
from .coordinator import IslamicPrayerDataUpdateCoordinator

SENSOR_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(key="Fajr", name="Fajr prayer"),
    SensorEntityDescription(key="Dhuhr", name="Dhuhr prayer"),
    SensorEntityDescription(key="Asr", name="Asr prayer"),
    SensorEntityDescription(key="Maghrib", name="Maghrib prayer"),
    SensorEntityDescription(key="Isha", name="Isha prayer"),
    SensorEntityDescription(key="Sunrise", name="Sunrise time"),
    SensorEntityDescription(key="Sunset", name="Sunset time"),
    SensorEntityDescription(key="Imsak", name="Imsak time"),
    SensorEntityDescription(key="Midnight", name="Midnight time"),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Islamic prayer times sensor platform."""
    coordinator = hass.data[DOMAIN]

    async_add_entities(
        IslamicPrayerTimeSensor(coordinator, description)
        for description in SENSOR_DESCRIPTIONS
    )


class IslamicPrayerTimeSensor(
    CoordinatorEntity[IslamicPrayerDataUpdateCoordinator], SensorEntity
):
    """Representation of an Islamic prayer time sensor."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_icon = PRAYER_TIMES_ICON
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: IslamicPrayerDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the Islamic prayer time sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = description.key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, "Islamic Prayer Times")},
            default_name="Islamic Prayer Times",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> datetime:
        """Return the state of the sensor."""
        return self.coordinator.data[self.entity_description.key]
