from Dev.LogicLayer.Service.Service import Service
from Dev.PresentationLayer.GUI import App

if __name__ == '__main__':
    service = Service()
    App(service).mainloop()
