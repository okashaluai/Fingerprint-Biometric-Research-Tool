from abc import abstractmethod

from Dev.LogicLayer.LogicObjects.Asset import Asset
from Dev.Utils import Interface


class IConverter(Interface):

    @abstractmethod
    def convert(self, asset: Asset) -> Asset:
        pass
