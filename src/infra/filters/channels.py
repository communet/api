from dataclasses import dataclass


@dataclass(eq=False, frozen=True)
class GetAllChannelsInfraFilters:
    limit: int = 10
    offset: int = 0
