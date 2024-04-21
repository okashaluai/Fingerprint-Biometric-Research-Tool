from Dev.Utils import Interface


class IDao(Interface):
    pass


class AssetDAO(IDao):
    pass


class TemplateDAO(AssetDAO):
    pass


class ImageDAO(AssetDAO):
    pass


class PrintingObjectDAO(AssetDAO):
    pass


class OperationDAO(IDao):
    pass


class ExperimentDAO(IDao):
    pass
