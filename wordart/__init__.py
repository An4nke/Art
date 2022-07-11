from krita import DockWidgetFactory, DockWidgetFactoryBase
from wordart.wordart import *

DOCKER_ID = 'DockerLinkGrepper'
instance = Krita.instance()

dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        DockerLinkGrepper)

instance.addDockWidgetFactory(dock_widget_factory)

