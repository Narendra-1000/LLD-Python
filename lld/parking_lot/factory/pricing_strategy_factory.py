from ..enums.pricing_strategy_type import PricingStrategyType
from ..strategy.pricing.event_based_pricing import EventBasedPricing
from ..strategy.pricing.pricing_strategy import PricingStrategy
from ..strategy.pricing.time_based_pricing import TimeBasedPricing


class PricingStrategyFactory:
    @staticmethod
    def get(strategy_type: PricingStrategyType) -> PricingStrategy:
        if strategy_type == PricingStrategyType.TIME_BASED:
            return TimeBasedPricing()
        if strategy_type == PricingStrategyType.EVENT_BASED:
            return EventBasedPricing()
        raise ValueError(f"Unsupported pricing strategy type: {strategy_type}")
