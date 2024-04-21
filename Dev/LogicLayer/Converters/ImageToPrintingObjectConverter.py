from Dev.LogicLayer.Converters.IConverter import IConverter
from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.PrintingObject import PrintingObject


class ImageToPrintingObjectConverter(IConverter):
    def convert(self, asset: Image) -> PrintingObject:
        raise NotImplementedError
