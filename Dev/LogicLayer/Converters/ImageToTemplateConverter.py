from Dev.LogicLayer.Converters.IConverter import IConverter
from Dev.LogicLayer.LogicObjects.Image import Image
from Dev.LogicLayer.LogicObjects.Template import Template


class ImageToTemplateConverter(IConverter):

    def convert(self, asset: Image) -> Template:
        raise NotImplementedError
