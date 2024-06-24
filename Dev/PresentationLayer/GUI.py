import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

import customtkinter
import open3d as o3d
from CTkMessagebox import CTkMessagebox
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

from Dev.DTOs import ImageDTO, ExperimentDTO, OperationDTO, TemplateDTO
from Dev.LogicLayer.Service.IService import IService
from Dev.PresentationLayer.tooltip import ToolTip
from Dev.Utils import Singleton

absolute_path = os.path.dirname(__file__)
assets_path = os.path.join(absolute_path, "Assets")


# Wrapper class for CustomTkinter and TkinterDnD
class Tk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


# Builds drag and drop / browse files widget
def build_drag_n_drop(frame, handle_choose_file, handle_choose_directory, choose_file_title, file_types,
                      choose_directory_title, invoke_reset_wrapper=None, width=240, height=80, view_function=None):
    main_frame = customtkinter.CTkFrame(
        master=frame,
        width=width,
        height=height,
        corner_radius=20,
        fg_color="transparent",
        bg_color="transparent"
    )

    def build_dnd_frame():
        dnd_frame = customtkinter.CTkFrame(
            master=main_frame,
            width=width,
            height=height,
            corner_radius=20,
            border_width=2,
        )
        dnd_frame.grid(row=0, column=0)
        dnd_frame.columnconfigure(0, weight=1)
        dnd_frame.rowconfigure((0, 4), weight=1)
        dnd_frame.drop_target_register(DND_FILES)

        def handle_drop(e):
            path = e.data
            if os.path.isdir(path):
                dnd_frame.destroy()
                build_selected_labels(path)
                handle_choose_directory(path)
            elif os.path.isfile(path):
                dnd_frame.destroy()
                build_selected_labels(path)
                handle_choose_file(path)

        dnd_frame.dnd_bind("<<Drop>>", handle_drop)

        return dnd_frame

    def build_selected_frame():
        selected_frame = customtkinter.CTkFrame(
            master=main_frame,
            width=width,
            height=height,
            corner_radius=20,
            border_width=2,
        )
        selected_frame.grid(row=0, column=0)
        selected_frame.columnconfigure(0, weight=1)
        return selected_frame

    def build_selected_labels(file_path):
        selected_frame = build_selected_frame()

        selected_label = customtkinter.CTkLabel(
            selected_frame,
            width=width,
            text=f"Selected {'Directory' if os.path.isdir(file_path) else 'File'}\n[ {os.path.basename(file_path)} ]",
            font=customtkinter.CTkFont(weight="bold", size=16)
        )
        selected_label.grid(row=1, column=0, sticky=customtkinter.EW, padx=10, pady=(20, 0))

        view_label = customtkinter.CTkLabel(
            selected_frame,
            width=width,
            text="View",
            cursor="hand2",
            text_color="dodger blue"
        )
        view_label.grid(row=2, column=0, sticky=customtkinter.EW, padx=10, pady=18)
        if view_function is not None:
            # def view(event):
            #     view_function()
            view_label.bind('<Button-1>', view_function)

        reset_label = customtkinter.CTkLabel(
            selected_frame,
            width=width,
            text="Reset",
            cursor="hand2",
            text_color="dodger blue"
        )
        reset_label.grid(row=3, column=0, sticky=customtkinter.EW, padx=10, pady=(0, 20))

        def handle_reset(e):
            selected_frame.destroy()
            build_dnd_labels()
            if invoke_reset_wrapper is not None:
                invoke_reset_wrapper()

        reset_label.bind('<Button-1>', handle_reset)

    def build_dnd_labels():
        dnd_frame = build_dnd_frame()

        dnd_label = customtkinter.CTkLabel(
            master=dnd_frame,
            text=f"Drag & drop files here...",
            corner_radius=20,
            width=width,
            font=customtkinter.CTkFont(slant='italic')
        )
        dnd_label.grid(row=1, column=0, sticky=customtkinter.EW, padx=10, pady=(20, 0))

        or_label = customtkinter.CTkLabel(
            master=dnd_frame,
            text="\nor\n",
            corner_radius=20,
            width=width,
        )
        or_label.grid(row=2, column=0, sticky=customtkinter.EW, padx=10)

        choose_file_label = customtkinter.CTkLabel(
            master=dnd_frame,
            text="Select File",
            corner_radius=20,
            width=width,
            cursor="hand2",
            text_color="dodger blue",
            font=customtkinter.CTkFont(underline=True)
        )
        choose_file_label.grid(row=3, column=0, sticky=customtkinter.EW, padx=10, pady=(0, 0))

        choose_directory_label = customtkinter.CTkLabel(
            master=dnd_frame,
            text="Select Directory",
            corner_radius=20,
            width=width,
            cursor="hand2",
            text_color="dodger blue",
            font=customtkinter.CTkFont(underline=True)
        )
        choose_directory_label.grid(row=4, column=0, sticky=customtkinter.EW, padx=10, pady=(0, 20))

        def handle_choose_file_event(e):
            file_path = filedialog.askopenfilename(title=choose_file_title, filetypes=file_types)
            if file_path:
                dnd_frame.destroy()
                build_selected_labels(file_path)
                handle_choose_file(file_path)

        def handle_choose_directory_event(e):
            directory_path = filedialog.askdirectory(title=choose_directory_title)
            if directory_path:
                dnd_frame.destroy()
                build_selected_labels(directory_path)
                handle_choose_directory(directory_path)

        choose_file_label.bind("<Button-1>", handle_choose_file_event)
        choose_directory_label.bind("<Button-1>", handle_choose_directory_event)

    build_dnd_labels()

    return main_frame


def view_stl_open3d(stl_path: str):
    mesh = o3d.io.read_triangle_mesh(stl_path)
    mesh = mesh.compute_vertex_normals()

    o3d.visualization.draw_geometries([mesh], window_name="Converted STL",
                                      width=800, height=800,
                                      left=int((Tk().winfo_screenwidth() - 800) / 2),
                                      top=int((Tk().winfo_screenheight() - 800) / 2))


def view_image(image_path: str):
    image = Image.open(image_path)
    image.show()


class SideMenuFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.grid_rowconfigure(5, weight=1)

        self.font = customtkinter.CTkFont(weight="bold")

        self.logo_label = customtkinter.CTkLabel(
            self, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.convert_assets_button = customtkinter.CTkButton(
            self, text="Convert Assets", font=customtkinter.CTkFont(weight="bold"), image=customtkinter.CTkImage(
                Image.open(os.path.join(assets_path, "file.png")),
                size=(25, 25)
            ), anchor='w',
            command=self.handle_convert_assets_button
        )
        self.convert_assets_button.grid(row=1, column=0, padx=20, pady=10, sticky=customtkinter.EW)

        self.match_templates_button = customtkinter.CTkButton(
            self, text="Match Templates", font=customtkinter.CTkFont(weight="bold"),
            image=customtkinter.CTkImage(
                Image.open(os.path.join(assets_path, "compare.png")),
                size=(25, 25)
            ), anchor='w',
            command=self.handle_match_template_button
        )
        self.match_templates_button.grid(row=2, column=0, padx=20, pady=10, sticky=customtkinter.EW)

        self.experiments_button = customtkinter.CTkButton(
            self, text="Experiments", font=customtkinter.CTkFont(weight="bold"), image=customtkinter.CTkImage(
                Image.open(os.path.join(assets_path, "chemistry.png")),
                size=(25, 25),
            ), anchor='w', command=self.handle_experiments_button
        )
        self.experiments_button.grid(row=3, column=0, padx=20, pady=10, sticky=customtkinter.EW)

        self.experiments_button = customtkinter.CTkButton(
            self, text="New Experiment", font=customtkinter.CTkFont(weight="bold"), image=customtkinter.CTkImage(
                Image.open(os.path.join(assets_path, "add.png")),
                size=(25, 25)
            ), anchor='w',
            command=self.handle_new_experiment_button
        )
        self.experiments_button.grid(row=4, column=0, padx=20, pady=10, sticky=customtkinter.EW)

        self.is_light_mode = False
        self.appearance_mode_switch = customtkinter.CTkSwitch(
            self, text="Dark Mode", font=customtkinter.CTkFont(weight="bold"), command=self.change_to_light_mode_event
        )
        self.appearance_mode_switch.grid(row=6, column=0, padx=20, pady=10)
        self.appearance_mode_switch.select()

        self.experiments_button = customtkinter.CTkButton(
            self, text="Info", font=customtkinter.CTkFont(weight="bold"), image=customtkinter.CTkImage(
                Image.open(os.path.join(assets_path, "info.png")),
                size=(25, 25)
            ), command=self.handle_experiments_button
        )
        self.experiments_button.grid(row=7, column=0, padx=20, pady=(10, 10), sticky=customtkinter.EW)

    def handle_convert_assets_button(self):
        self.master.convert_assets_frame.tkraise()

    def handle_match_template_button(self):
        self.master.match_templates_frame.tkraise()

    def handle_experiments_button(self):
        self.master.experiments_frame.tkraise()

        # add 10 experiments for mock
        for i in range(10):
            response = service.create_experiment(f"experiment {uuid.uuid1()}")
            if response.success:
                print(f"{response.data.experiment_name}")
                service.set_current_experiment(response.data.experiment_id)
                if i % 2 == 0:
                    convert_response1 = service.convert_image_to_template(
                        ImageDTO(None, r"C:\Users\Yazan\Desktop\109_1_8bit.png", datetime.now())
                    )
                    convert_response2 = service.convert_image_to_template(
                        ImageDTO(None, r"C:\Users\Yazan\Desktop\Final_Project\Dev\Tests\Assets\Images\109_2_8bit.png",
                                 datetime.now())
                    )
                    if convert_response1.success and convert_response2.success:
                        print(convert_response1.data.path)
                        print(convert_response2.data.path)
                    print(len(service.get_current_experiment().data.operations))
                # else:
                #     convert_response = service.convert_image_to_template(
                #         ImageDTO(None, r"C:\Users\Yazan\Desktop\Final_Project\Dev\Tests\Assets\Images\109_2_8bit.png",
                #                  datetime.now())
                #     )

            else:
                print(response.error)

        self.master.experiments_frame.load_experiments()

    def handle_new_experiment_button(self):
        self.master.new_experiment_frame.tkraise()

    def change_to_light_mode_event(self):
        if not self.is_light_mode:
            self.is_light_mode = True
            customtkinter.set_appearance_mode("Light")
        else:
            self.is_light_mode = False
            customtkinter.set_appearance_mode("Dark")


class ConvertAssetsFrame(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Create tabview
        self.tabview = self.TabViewFrame(master=self)
        self.tabview.grid(row=0, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")

    class TabViewFrame(customtkinter.CTkTabview):
        def __init__(self, master):
            super().__init__(master=master)

            self.template_tab = self.TemplateTab(self)
            self.template_tab_frame = self.template_tab.frame

            self.image_tab = self.ImageTab(self)
            self.image_tab_frame = self.image_tab.frame

        class TemplateTab:
            def __init__(self, master):
                self.frame = master.add("Template")
                self.frame.grid_columnconfigure(0, weight=1)
                self.frame.grid_rowconfigure(0, weight=1)

                # Template import frame
                self.template_import_frame = self.TemplateImportFrame(parent_tab=self)
                self.template_import_frame.grid(
                    row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                )

                self.image_export_frame = None
                self.printing_object_export_frame = None

                # Default frame
                self.template_import_frame.tkraise()

            def build_printing_object_export_frame(self, path):
                # Printing object export frame
                self.printing_object_export_frame = self.PrintingObjectExportFrame(parent_tab=self, path=path)
                self.printing_object_export_frame.grid(
                    row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                )
                self.printing_object_export_frame.tkraise()

            def build_image_export_frame(self, path):
                # Image export frame
                self.image_export_frame = self.ImageExportFrame(parent_tab=self, path=path)
                self.image_export_frame.grid(
                    row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                )
                self.image_export_frame.tkraise()

            class ImageExportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab, path):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 7), weight=1)

                    self.image_path = path

                    self.title = customtkinter.CTkLabel(self, text="Image",
                                                        font=customtkinter.CTkFont(size=20, weight="bold"))
                    self.title.grid(row=1, column=1, padx=(20, 20), pady=(0, 20))

                    self.name = customtkinter.CTkLabel(self, text=f"[ {os.path.basename(path)} ]",
                                                       font=customtkinter.CTkFont(size=14))
                    self.name.grid(row=2, column=1, padx=(20, 20), pady=(20, 5))

                    self.view_label = customtkinter.CTkLabel(
                        self,
                        text="View",
                        cursor="hand2",
                        text_color="dodger blue"
                    )
                    self.view_label.grid(row=3, column=1, padx=(20, 20), pady=(5, 20))
                    self.view_label.bind('<Button-1>', self.view_image)

                    self.export_button = customtkinter.CTkButton(self, text="Export")
                    self.export_button.grid(row=4, column=1, padx=(20, 20), pady=5)

                    self.export_button = customtkinter.CTkButton(
                        self,
                        text="Convert to 3D Object",
                        command=self.handle_convert_to_printing_object_button,
                    )
                    self.export_button.grid(row=5, column=1, padx=(20, 20), pady=5)

                    self.back_button = customtkinter.CTkButton(
                        self, text="Back", command=self.handle_back_button
                    )
                    self.back_button.grid(row=6, column=1, padx=(20, 20), pady=5)

                def handle_convert_to_printing_object_button(self):
                    image_dto = ImageDTO(None, self.image_path, datetime.now())
                    response = service.convert_image_to_printing_object(image_dto)
                    if response.success:
                        self.parent_tab.build_printing_object_export_frame(path=response.data.path)
                    else:
                        CTkMessagebox(icon="cancel", title="Image Converter Error", message=response.error)

                def view_image(self, event=None):
                    view_image(self.image_path)

                def handle_back_button(self):
                    self.parent_tab.template_import_frame.tkraise()

            class PrintingObjectExportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab, path):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 6), weight=1)

                    self.stl_path = path

                    self.title = customtkinter.CTkLabel(self, text="Printing Object",
                                                        font=customtkinter.CTkFont(size=20, weight="bold"))
                    self.title.grid(row=1, column=1, padx=(20, 20), pady=(0, 20))

                    self.name = customtkinter.CTkLabel(self, text=f"[ {os.path.basename(path)} ]",
                                                       font=customtkinter.CTkFont(size=14))
                    self.name.grid(row=2, column=1, padx=(20, 20), pady=(20, 5))

                    self.view_label = customtkinter.CTkLabel(
                        self,
                        text="View",
                        cursor="hand2",
                        text_color="dodger blue"
                    )
                    self.view_label.grid(row=3, column=1, padx=(20, 20), pady=(5, 20))
                    self.view_label.bind('<Button-1>', self.view_stl)

                    self.export_button = customtkinter.CTkButton(self, text="Export")
                    self.export_button.grid(row=4, column=1, padx=(20, 20), pady=5)

                    self.back_button = customtkinter.CTkButton(
                        self, text="Back", command=self.handle_back_button
                    )
                    self.back_button.grid(row=5, column=1, padx=(20, 20), pady=5)

                def view_stl(self, event=None):
                    view_stl_open3d(self.stl_path)

                def handle_back_button(self):
                    self.parent_tab.image_export_frame.tkraise()

            class TemplateImportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 4), weight=1)

                    self.template_path = None

                    self.dnd = build_drag_n_drop(
                        self,
                        handle_choose_directory=self.handle_choose_directory,
                        handle_choose_file=self.handle_choose_file,
                        choose_file_title="Choose a template file",
                        file_types=[("Text files", "*.txt"), ("All files", "*.*")],
                        choose_directory_title="Choose a templates directory",
                        invoke_reset_wrapper=self.handle_reset
                    )
                    self.dnd.grid(row=0, column=1, padx=(20, 20), pady=5)

                    self.convert_to_image_button = customtkinter.CTkButton(
                        self,
                        text="Convert to Image",
                        command=self.handle_convert_to_image_button,
                    )
                    self.convert_to_image_button.grid(
                        row=1, column=1, padx=(20, 20), pady=5
                    )
                    self.convert_to_image_button.configure(state=customtkinter.DISABLED)

                def handle_reset(self):
                    self.convert_to_image_button.configure(state=customtkinter.DISABLED)

                def handle_choose_file(self, path):
                    self.convert_to_image_button.configure(state=customtkinter.NORMAL)
                    self.template_path = path

                def handle_choose_directory(self, path):
                    self.convert_to_image_button.configure(state=customtkinter.NORMAL)
                    self.template_path = path

                def handle_convert_to_image_button(self):
                    template_dto = TemplateDTO(None, self.template_path, datetime.now())
                    response = service.convert_template_to_image(template_dto)
                    if response.success:
                        self.parent_tab.build_image_export_frame(response.data.path)
                    else:
                        CTkMessagebox(icon="cancel", title="Template Converter Error", message=response.error)

        class ImageTab:
            def __init__(self, master):
                self.frame = master.add("Image")
                self.frame.grid_columnconfigure(0, weight=1)
                self.frame.grid_rowconfigure(0, weight=1)

                # Image import frame
                self.image_import_frame = self.ImageImportFrame(parent_tab=self)
                self.image_import_frame.grid(
                    row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                )

                # Default frame
                self.image_import_frame.tkraise()

            def build_printing_object_export_frame(self, path):
                # Printing object export frame
                printing_object_export_frame = self.PrintingObjectExportFrame(parent_tab=self, path=path)
                printing_object_export_frame.grid(
                    row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                )
                printing_object_export_frame.tkraise()

            def build_template_export_frame(self, path):
                # Template export frame
                template_export_frame = self.TemplateExportFrame(parent_tab=self, path=path)
                template_export_frame.grid(
                    row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                )
                template_export_frame.tkraise()

            class TemplateExportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab, path):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 6), weight=1)

                    self.template_path = path

                    self.title = customtkinter.CTkLabel(self, text="Template",
                                                        font=customtkinter.CTkFont(size=20, weight="bold"))
                    self.title.grid(row=1, column=1, padx=(20, 20), pady=(0, 20))

                    self.name = customtkinter.CTkLabel(self, text=f"[ {os.path.basename(path)} ]",
                                                       font=customtkinter.CTkFont(size=14))
                    self.name.grid(row=2, column=1, padx=(20, 20), pady=(20, 5))

                    self.view_label = customtkinter.CTkLabel(
                        self,
                        text="View",
                        cursor="hand2",
                        text_color="dodger blue"
                    )
                    self.view_label.grid(row=3, column=1, padx=(20, 20), pady=(5, 20))
                    self.view_label.bind('<Button-1>', self.view_template)

                    self.export_button = customtkinter.CTkButton(self, text="Export", command=self.handle_export_button)
                    self.export_button.grid(row=4, column=1, padx=(20, 20), pady=5)

                    self.back_button = customtkinter.CTkButton(
                        self, text="Back", command=self.handle_back_button
                    )
                    self.back_button.grid(row=5, column=1, padx=(20, 20), pady=5)

                def handle_back_button(self):
                    self.destroy()
                    self.parent_tab.image_import_frame.tkraise()

                def view_template(self, e):
                    pass

                def handle_export_button(self):
                    file_path = filedialog.asksaveasfilename(title="Export Template",
                                                             filetypes=(("All Files", "*.*"),),
                                                             initialfile=Path(self.template_path).stem)
                    if file_path:
                        shutil.copytree(self.template_path, os.path.dirname(file_path), dirs_exist_ok=True)

            class PrintingObjectExportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab, path):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 6), weight=1)

                    self.stl_path = path

                    self.title = customtkinter.CTkLabel(self, text="Printing Object",
                                                        font=customtkinter.CTkFont(size=20, weight="bold"))
                    self.title.grid(row=1, column=1, padx=(20, 20), pady=(0, 20))

                    self.name = customtkinter.CTkLabel(self, text=f"[ {os.path.basename(path)} ]",
                                                       font=customtkinter.CTkFont(size=14))
                    self.name.grid(row=2, column=1, padx=(20, 20), pady=(20, 5))

                    self.view_label = customtkinter.CTkLabel(
                        self,
                        text="View",
                        cursor="hand2",
                        text_color="dodger blue"
                    )
                    self.view_label.grid(row=3, column=1, padx=(20, 20), pady=(5, 20))
                    self.view_label.bind('<Button-1>', self.view_stl)

                    self.export_button = customtkinter.CTkButton(self, text="Export", command=self.handle_export_button)
                    self.export_button.grid(row=4, column=1, padx=(20, 20), pady=5)

                    self.back_button = customtkinter.CTkButton(
                        self, text="Back", command=self.handle_back_button
                    )
                    self.back_button.grid(row=5, column=1, padx=(20, 20), pady=5)

                def handle_back_button(self):
                    self.destroy()
                    self.parent_tab.image_import_frame.tkraise()

                def view_stl(self, e):
                    view_stl_open3d(self.stl_path)

                def handle_export_button(self):
                    file_path = filedialog.asksaveasfilename(title="Export STL",
                                                             filetypes=(("STL Files", ".stl"),),
                                                             initialfile=Path(self.stl_path).stem)
                    if file_path:
                        shutil.copy(self.stl_path, f"{file_path}.stl")

            class ImageImportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 5), weight=1)

                    self.image_path = None

                    self.convert_to_template_button = customtkinter.CTkButton(
                        self,
                        text="Convert to Template",
                        command=self.handle_convert_to_template_button,
                    )
                    self.convert_to_template_button.grid(
                        row=1, column=1, padx=(20, 20), pady=5
                    )

                    self.convert_to_printing_object_button = customtkinter.CTkButton(
                        self,
                        text="Convert to 3D Object",
                        command=self.handle_convert_to_printing_object_button,
                    )
                    self.convert_to_printing_object_button.grid(
                        row=2, column=1, padx=(20, 20), pady=5
                    )

                    self.convert_to_template_button.configure(state=customtkinter.DISABLED)
                    self.convert_to_printing_object_button.configure(state=customtkinter.DISABLED)

                    self.dnd = build_drag_n_drop(
                        self,
                        handle_choose_directory=self.handle_choose_directory,
                        handle_choose_file=self.handle_choose_file,
                        choose_file_title="Choose a template file",
                        file_types=[("Text files", "*.txt"), ("All files", "*.*")],
                        choose_directory_title="Choose a templates directory",
                        invoke_reset_wrapper=self.handle_reset,
                        view_function=self.view_image_event,
                    )
                    self.dnd.grid(row=0, column=1, padx=(20, 20), pady=5)

                def view_image_event(self, event=None):
                    view_image(self.image_path)

                def handle_reset(self):
                    self.convert_to_template_button.configure(state=customtkinter.DISABLED)
                    self.convert_to_printing_object_button.configure(state=customtkinter.DISABLED)

                def handle_choose_file(self, path):
                    self.convert_to_template_button.configure(state=customtkinter.NORMAL)
                    self.convert_to_printing_object_button.configure(state=customtkinter.NORMAL)
                    self.image_path = path

                def handle_choose_directory(self, path):
                    self.convert_to_template_button.configure(state=customtkinter.NORMAL)
                    self.convert_to_printing_object_button.configure(state=customtkinter.NORMAL)
                    self.image_path = path

                def handle_convert_to_template_button(self):
                    image_dto = ImageDTO(None, self.image_path, datetime.now())
                    response = service.convert_image_to_template(image_dto)
                    if response.success:
                        self.parent_tab.build_template_export_frame(response.data.path)
                    else:
                        CTkMessagebox(icon="cancel", title="Image Converter Error", message=response.error)

                def handle_convert_to_printing_object_button(self):
                    image_dto = ImageDTO(None, self.image_path, datetime.now())
                    response = service.convert_image_to_printing_object(image_dto)
                    if response.success:
                        self.parent_tab.build_printing_object_export_frame(response.data.path)
                    else:
                        CTkMessagebox(icon="cancel", title="Image Converter Error", message=response.error)


class MatchTemplatesFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Subframe
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(
            row=0,
            column=0,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(20, 20),
        )
        self.frame.grid_columnconfigure((0, 3), weight=1)
        self.frame.grid_rowconfigure((0, 6), weight=1)

        self.results_frame = None

        self.f1_is_selected = False
        self.f2_is_selected = False
        self.dir1_is_selected = False
        self.dir2_is_selected = False

        self.path_set1 = None
        self.path_set2 = None

        def handle_reset1():
            self.f1_is_selected = False
            self.dir1_is_selected = False
            self.path_set1 = None
            self.match_button.configure(state=customtkinter.DISABLED)

        def handle_reset2():
            self.f2_is_selected = False
            self.dir2_is_selected = False
            self.path_set2 = None
            self.match_button.configure(state=customtkinter.DISABLED)

        def handle_choose_file1(path):
            self.f1_is_selected = True
            if self.f2_is_selected or self.dir2_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set1 = path

        def handle_choose_directory1(path):
            self.dir1_is_selected = True
            if self.f2_is_selected or self.dir2_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set1 = path

        font = customtkinter.CTkFont(size=16, weight="bold")
        customtkinter.CTkLabel(self.frame, text="First Set", font=font).grid(row=2, column=1, padx=(20, 20),
                                                                             sticky=customtkinter.EW, pady=5)
        self.dnd1 = build_drag_n_drop(
            self.frame,
            handle_choose_directory=handle_choose_directory1,
            handle_choose_file=handle_choose_file1,
            choose_file_title="Choose a template file",
            file_types=[("Text files", "*.txt"), ("All files", "*.*")],
            choose_directory_title="Choose a templates directory",
            invoke_reset_wrapper=handle_reset1
        )
        self.dnd1.grid(row=3, column=1, padx=(20, 20), pady=5)

        customtkinter.CTkLabel(self.frame, text="Second Set", font=font).grid(row=2, column=2, padx=(20, 20),
                                                                              sticky=customtkinter.EW, pady=5)

        def handle_choose_file2(path):
            self.f2_is_selected = True
            if self.f1_is_selected or self.dir1_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set2 = path

        def handle_choose_directory2(path):
            self.dir2_is_selected = True
            if self.f1_is_selected or self.dir1_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set2 = path

        self.dnd2 = build_drag_n_drop(
            self.frame,
            handle_choose_directory=handle_choose_directory2,
            handle_choose_file=handle_choose_file2,
            choose_file_title="Choose a template file",
            file_types=[("Text files", "*.txt"), ("All files", "*.*")],
            choose_directory_title="Choose a templates directory",
            invoke_reset_wrapper=handle_reset2
        )
        self.dnd2.grid(row=3, column=2, padx=(20, 20), pady=5)

        self.match_button = customtkinter.CTkButton(self.frame, text="Match Templates",
                                                    command=self.handle_match_templates_button)
        self.match_button.grid(
            row=4,
            columnspan=4,
            padx=(20, 20),
            pady=(40, 5)
        )
        self.match_button.configure(state=customtkinter.DISABLED)

    def handle_match_templates_button(self):
        if self.f1_is_selected and self.f2_is_selected:
            response = service.match_one_to_one(self.path_set1, self.path_set2)
        elif self.f1_is_selected and self.dir2_is_selected:
            response = service.match_one_to_many(self.path_set1, self.path_set2)
        elif self.f2_is_selected and self.dir1_is_selected:
            response = service.match_one_to_many(self.path_set2, self.path_set1)
        elif self.dir1_is_selected and self.dir2_is_selected:
            response = service.match_many_to_many(self.path_set1, self.path_set2)
        else:
            CTkMessagebox(icon="cancel", title="Unexpected Error", message="Unexpected GUI Error")

        if response.success:
            self.build_results_frame(response.data)
        else:
            CTkMessagebox(icon="cancel", title="Matching Error", message=response.error)

    def build_results_frame(self, results):
        self.results_frame = customtkinter.CTkFrame(self)
        self.results_frame.grid_columnconfigure((0), weight=1)
        self.results_frame.grid_rowconfigure((0, 4), weight=1)
        self.results_frame.grid(
            row=0,
            column=0,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(20, 20),
        )
        title = customtkinter.CTkLabel(self.results_frame, text="Matching Results",
                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        title.grid(row=0, column=0, padx=(20, 20), sticky=customtkinter.EW, pady=5)

        res_text = "Export to View Matching Results."
        if self.f1_is_selected and self.f2_is_selected:
            res_text = f"Score: {results}"
        results_label = customtkinter.CTkLabel(self.results_frame, text=res_text,
                                               font=customtkinter.CTkFont(size=16, weight="bold"))
        results_label.grid(row=1, column=0, padx=(20, 20), sticky=customtkinter.EW, pady=10)

        def handle_export_results():
            export_full_path = filedialog.asksaveasfilename(title="Export Matching Results",
                                                            filetypes=(("All Files", "*.*"),),
                                                            initialfile="MatchingScores.csv")
            if export_full_path == "" or None:
                return

            if self.f1_is_selected and self.f2_is_selected:
                response = service.export_matching_one_to_one_csv(self.path_set1, self.path_set2, results,
                                                                  export_full_path)
            else:
                response = service.export_matching_matrix_csv(results, export_full_path)

            if response.success:
                CTkMessagebox(icon="check", title="Export Successful", message="Matching scores exported successfully!")
            else:
                CTkMessagebox(icon="cancel", title="Export Error", message=response.error)

        export_button = customtkinter.CTkButton(self.results_frame, text="Export CSV", command=handle_export_results)
        export_button.grid(
            row=2,
            column=0,
            padx=(20, 20),
            pady=(40, 5)
        )

        def handle_back_button():
            self.results_frame.destroy()

        back_button = customtkinter.CTkButton(self.results_frame, text="Back", command=handle_back_button)
        back_button.grid(
            row=3,
            column=0,
            padx=(20, 20),
            pady=(5, 5)
        )


class OperationRowFrame(customtkinter.CTkFrame):
    def __init__(self, master, index: int, operation_dto: OperationDTO, experiment_frame: customtkinter.CTkFrame):
        super().__init__(
            master=master, corner_radius=10, fg_color="transparent"
        )
        self.columnconfigure((0, 1, 2), weight=1)

        self.index = index
        self.experiment_frame = experiment_frame

        self.input_label = customtkinter.CTkLabel(
            self, text=f"Input: {operation_dto.operation_input.path}"
        )
        self.input_label.grid(
            row=0, column=0, sticky=customtkinter.EW, padx=(20, 20)
        )

        self.output_label = customtkinter.CTkLabel(self, text=f"Output: {operation_dto.operation_output.path}")
        self.output_label.grid(
            row=0, column=1, sticky=customtkinter.EW, padx=(20, 20)
        )

        formatted_date = operation_dto.operation_date.strftime("%d/%m/%Y    %H:%M:%S")
        self.date_label = customtkinter.CTkLabel(
            self, text=f"Date: {formatted_date})"
        )
        self.date_label.grid(
            row=0, column=2, sticky=customtkinter.EW, padx=(20, 20)
        )

        self.delete_button = customtkinter.CTkLabel(
            self,
            text="",
            cursor="hand2",
            image=customtkinter.CTkImage(
                Image.open(os.path.join(assets_path, "icons8-remove-80.png")),
                size=(25, 25)
            ),
        )
        self.delete_button.bind('<Button-1>', command=self.handle_delete_operation)
        self.delete_button.grid(
            row=0, column=3, padx=(10, 25), pady=10
        )
        self.tp1 = ToolTip(self.delete_button, msg="Delete Operation", delay=1.0)

        self.operation_dto = operation_dto

    def destroy_tooltips(self):
        self.tp1.destroy()

    def handle_delete_operation(self, event=None):
        response = service.delete_operation(
            self.experiment_frame.experiment_dto.experiment_id,
            self.operation_dto.operation_id)
        if response.success:
            for o in self.experiment_frame.experiment_dto.operations:
                if o.operation_id == self.operation_dto.operation_id:
                    self.experiment_frame.experiment_dto.operations.remove(o)

            self.destroy_tooltips()
            self.destroy()

            CTkMessagebox(icon="check", title="Operation",
                          message=f"Operation deleted successfully!")
        else:
            CTkMessagebox(icon="cancel", title="Operations Error", message=response.error)


class ExperimentsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Subframe
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(
            row=0,
            column=0,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(20, 20),
        )
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.search_entry = customtkinter.CTkEntry(
            self.frame, placeholder_text="Experiment name"
        )
        self.search_entry.grid(
            row=0,
            column=0,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(20, 20),
        )
        self.search_entry.bind('<Key>', self.search)

        self.search_button = customtkinter.CTkButton(
            self.frame, text="Search", command=self.search
        )
        self.search_button.grid(
            row=0,
            column=1,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(0, 20),
            pady=(20, 20),
        )

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.frame, label_text="Experiments", label_font=customtkinter.CTkFont(weight="bold", size=16)
        )
        self.scrollable_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(0, 20),
        )
        self.scrollable_frame.columnconfigure(0, weight=1)

        self.experiment_dtos = None

        self.experiments_frames = []

        global experiments_frame
        experiments_frame = self

    def show_experiments_on_frame(self, experiment_dtos: list[ExperimentDTO]):
        # Delete old experiment frames
        for ef in self.experiments_frames:
            ef.destroy_tooltips()
            for of in ef.operations_frames:
                of.destroy_tooltips()
                of.destroy()
            ef.destroy()

        # Build new frames
        for i, e in enumerate(experiment_dtos):
            row_frame = self.ExperimentRowFrame(
                self.scrollable_frame, index=i, experiment_dto=e
            )
            row_frame.grid(
                row=i,
                column=0,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(20, 20),
                pady=(0, 20),
            )
            self.experiments_frames.append(row_frame)

    def load_experiments(self):
        response = service.get_experiments()
        if response.success:
            self.experiment_dtos = response.data
            self.show_experiments_on_frame(self.experiment_dtos)
        else:
            CTkMessagebox(icon="cancel", title="Experiments Error", message=response.error)

    def search(self, e=None):
        def get_searchable_string(string: str):
            ignore_chars = [" ", "'", "!", ".", ",", "-", "_", "(", ")", "*", "@", "%", "#", "^", "&", "+", "~"]

            searchable_string = string
            for ic in ignore_chars:
                searchable_string = searchable_string.replace(ic, "")

            return searchable_string

        keyword = self.search_entry.get()

        filtered_experiments_list: list[ExperimentDTO] = []

        for e in self.experiment_dtos:
            # filter experiments according to its name
            k = get_searchable_string(keyword)
            en = get_searchable_string(e.experiment_name)
            if k in en:
                filtered_experiments_list.append(e)

        self.show_experiments_on_frame(filtered_experiments_list)

    class ExperimentRowFrame(customtkinter.CTkFrame):
        def __init__(self, master, index: int, experiment_dto: ExperimentDTO):
            super().__init__(
                master=master, corner_radius=10, border_width=2,
            )
            self.index = index
            self.columnconfigure((0), weight=1)
            self.rowconfigure(3, weight=1)

            self.experiment_dto = experiment_dto
            self.experiment_name = experiment_dto.experiment_name
            self.experiment_date = experiment_dto.experiment_date.strftime("%d/%m/%Y    %H:%M:%S")
            self.experiment_info = customtkinter.CTkLabel(self,
                                                          text=f"{self.experiment_name}    {self.experiment_date}")
            self.experiment_info.grid(row=0, column=0, sticky=customtkinter.EW, padx=(20, 10), pady=10)

            self.continue_experiment = customtkinter.CTkLabel(
                self,
                text="",
                cursor="hand2",
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "arrows.png")),
                    size=(25, 25)
                ),
            )
            self.continue_experiment.bind('<Button-1>', command=self.handle_continue_experiment)
            self.continue_experiment.grid(
                row=0, column=1, padx=(20, 10), pady=10
            )
            self.tp1 = ToolTip(self.continue_experiment, msg="Continue Experiment", delay=1.0)

            self.edit_experiment = customtkinter.CTkLabel(
                self,
                text="",
                cursor="hand2",
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "pen.png")),
                    size=(25, 25)
                ),
            )
            self.edit_experiment.bind('<Button-1>', command=self.handle_edit_experiment)
            self.edit_experiment.grid(
                row=0, column=2, padx=(10, 10), pady=10
            )
            self.tp2 = ToolTip(self.edit_experiment, msg="Edit Experiment", delay=1.0)

            self.save_experiment = None
            self.tp_save_experiment = None

            self.delete_button = customtkinter.CTkLabel(
                self,
                text="",
                cursor="hand2",
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "icons8-remove-80.png")),
                    size=(25, 25)
                ),
            )
            self.delete_button.bind('<Button-1>', command=self.handle_delete_experiment)
            self.delete_button.grid(
                row=0, column=3, padx=(10, 25), pady=10
            )
            self.tp3 = ToolTip(self.delete_button, msg="Delete Experiment", delay=1.0)

            self.operations_dtos = None
            self.operations_frames = []
            self.scrollable_frame_wrapper = None
            self.scrollable_frame = None
            self.search_entry = None
            self.search_button = None
            self.edit_mode = False

        def build_edit_experiment_frame(self):
            self.save_experiment = customtkinter.CTkLabel(
                self,
                text="",
                cursor="hand2",
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "save.png")),
                    size=(25, 25)
                ),
            )
            self.save_experiment.bind('<Button-1>', command=self.handle_edit_experiment)
            self.save_experiment.grid(
                row=0, column=2, padx=(10, 10), pady=10
            )
            self.tp_save_experiment = ToolTip(self.save_experiment, msg="Save", delay=1.0)

            self.search_entry = customtkinter.CTkEntry(
                self, placeholder_text="Search file or directory names"
            )
            self.search_entry.grid(
                row=2,
                column=0,
                columnspan=3,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(20, 20),
                pady=(20, 20),
            )
            self.search_entry.bind('<Key>', self.search)

            self.search_button = customtkinter.CTkButton(
                self, text="Search", command=self.search
            )
            self.search_button.grid(
                row=2,
                column=3,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(0, 20),
                pady=(20, 20),
            )

            self.scrollable_frame_wrapper = customtkinter.CTkFrame(self, bg_color="transparent", fg_color="transparent")
            self.scrollable_frame_wrapper.grid(
                row=3,
                columnspan=4,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(20, 20),
                pady=(0, 20),
            )
            self.scrollable_frame_wrapper.columnconfigure(0, weight=1)

            self.scrollable_frame = customtkinter.CTkScrollableFrame(
                self.scrollable_frame_wrapper, label_text="Operations",
                label_font=customtkinter.CTkFont(weight="bold", size=16)
            )
            self.scrollable_frame.grid(
                row=0,
                column=0,
                sticky=customtkinter.NS + customtkinter.EW,
            )
            self.scrollable_frame.columnconfigure(0, weight=1)

        def show_operations_on_frame(self, operations_dtos: list[OperationDTO]):
            # Delete old operation frames
            for of in self.operations_frames:
                of.destroy_tooltips()
                of.destroy()

            # Build new frames
            for i, o in enumerate(operations_dtos):
                row_frame = OperationRowFrame(
                    self.scrollable_frame, index=i, operation_dto=o, experiment_frame=self,
                )
                row_frame.grid(
                    row=i,
                    column=0,
                    sticky=customtkinter.NS + customtkinter.EW,
                    padx=(20, 20),
                    pady=(0, 20),
                )
                self.operations_frames.append(row_frame)

        def load_operations(self):
            self.operations_dtos = self.experiment_dto.operations
            print(self.operations_dtos)
            self.show_operations_on_frame(self.operations_dtos)

        def search(self, event=None):
            def get_searchable_string(string: str):
                ignore_chars = [" ", "'", "!", ".", ",", "-", "_", "(", ")", "*", "@", "%", "#", "^", "&", "+", "~"]

                searchable_string = string
                for ic in ignore_chars:
                    searchable_string = searchable_string.replace(ic, "")

                return searchable_string

            keyword = self.search_entry.get()

            filtered_operations_list: list[OperationDTO] = []

            for o in self.operations_dtos:
                # filter operations according to its name
                k = get_searchable_string(keyword)
                on1 = get_searchable_string(o.operation_input.path)
                on2 = get_searchable_string(o.operation_output.path)
                if k in on1 or on2:
                    filtered_operations_list.append(o)

            self.show_operations_on_frame(filtered_operations_list)

        def destroy_tooltips(self):
            self.tp1.destroy()
            self.tp2.destroy()
            self.tp3.destroy()

        def handle_edit_experiment(self, event=None):
            if self.edit_mode:
                self.edit_mode = False
                self.search_button.destroy()
                self.search_entry.destroy()
                for of in self.operations_frames:
                    of.destroy()
                self.scrollable_frame.destroy()
                self.scrollable_frame_wrapper.destroy()
                self.tp_save_experiment.destroy()
                self.save_experiment.destroy()
                self.tp2 = ToolTip(self.edit_experiment, msg="Edit Experiment", delay=1.0)
            else:
                self.edit_mode = True
                self.build_edit_experiment_frame()
                self.load_operations()

        def handle_continue_experiment(self, e):
            response = service.set_current_experiment(self.experiment_name)
            if response.success:
                CTkMessagebox(icon="check", title="Experiment",
                              message=f"Current experiment is set to {self.experiment_name} !")
            else:
                CTkMessagebox(icon="cancel", title="Experiments Error", message=response.error)

        def handle_delete_experiment(self, event=None):
            delete_response = service.delete_experiment(self.experiment_dto.experiment_id)
            if delete_response.success:
                for e in experiments_frame.experiment_dtos:
                    if e.experiment_id == self.experiment_dto.experiment_id:
                        experiments_frame.experiment_dtos.remove(e)

                self.destroy_tooltips()
                self.destroy()

                CTkMessagebox(icon="check", title="Experiment",
                              message=f"Experiment {self.experiment_name} deleted successfully!")
            else:
                CTkMessagebox(icon="cancel", title="Experiments Error", message=delete_response.error)


class NewExperimentFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Subframe
        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(
            row=0,
            column=0,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(20, 20),
        )
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure((0, 5), weight=1)

        self.label = customtkinter.CTkLabel(self.frame, text="Create New Experiment",
                                            font=customtkinter.CTkFont(weight="bold", size=20))
        self.label.grid(row=1, column=0, padx=(20, 20), pady=(0, 10))

        self.new_experiment_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Experiment Name", width=300,
                                                           justify=customtkinter.CENTER)
        self.new_experiment_entry.grid(row=2, column=0, padx=(20, 20), pady=(10, 10))

        self.new_experiment_button = customtkinter.CTkButton(self.frame, text="Create",
                                                             command=self.handle_create_new_experiment_button)
        self.new_experiment_button.grid(row=3, column=0, padx=(20, 20), pady=(10, 10))

        self.continue_experiment_button = customtkinter.CTkLabel(self.frame, text="Continue from existing experiment?",
                                                                 cursor="hand2", text_color="dodger blue2")
        self.continue_experiment_button.grid(row=4, column=0, padx=(20, 20), pady=(10, 40))
        self.continue_experiment_button.bind('<Button-1>', self.handle_continue_experiment_button)

    def handle_create_new_experiment_button(self):
        response = service.create_experiment(self.new_experiment_entry.get())
        if response.success:
            c = CTkMessagebox(icon="check", title="Experiment", message=f"Experiment created successfully!")

            if c.get() == "OK":
                msg = CTkMessagebox(title="Experiment", message="Do you want to start with this experiment?",
                                    icon="question", option_1="Yes", option_2="No")
                msg_response = msg.get()

                if msg_response == "Yes":
                    response = service.set_current_experiment(response.data.experiment_id)
                    if response.success:
                        CTkMessagebox(icon="check", title="Experiment",
                                      message=f"Current experiment is set to {response.data.experiment_name} successfully!")

                        App(service).change_current_experiment_name(response.data.experiment_name)
                    else:
                        CTkMessagebox(icon="cancel", title="Experiment Error", message=response.error)
        else:
            CTkMessagebox(icon="cancel", title="Experiment Error", message=response.error)

    def handle_continue_experiment_button(self, e):
        self.master.experiments_frame.tkraise()


class App(Tk, metaclass=Singleton):
    def __init__(self, _service: IService, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set system service
        global service
        service = _service

        # Current experiment name
        global experiment_name
        experiment_name = "Demo Experiment"

        # Configure app window
        app_width = 900
        app_height = 500
        self.minsize(width=app_width, height=app_height)
        self.app_name = "Fingerprint Biometrics Research Tool"
        self.title(f"{self.app_name} - [ {experiment_name} ]")
        self.update_idletasks()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = self.winfo_width() + 2 * frm_width
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        # win_height = self.winfo_height() + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - app_width // 2
        y = self.winfo_screenheight() // 2 - app_height // 2
        self.geometry("{}x{}+{}+{}".format(app_width, app_height, x, y))
        self.deiconify()

        # Default Appearance mode and colors
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        # Configure app grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar menu frame
        self.side_menu_frame = SideMenuFrame(master=self)
        self.side_menu_frame.grid(
            row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
        )

        # Uniform main frame grid config
        def main_frame_grid_config(frame):
            frame.grid(
                row=0, column=1, sticky=customtkinter.NS + customtkinter.EW, padx=(5, 0)
            )

        # Convert assets main frame
        self.convert_assets_frame = ConvertAssetsFrame(master=self)
        main_frame_grid_config(self.convert_assets_frame)

        # Match templates main frame
        self.match_templates_frame = MatchTemplatesFrame(master=self)
        main_frame_grid_config(self.match_templates_frame)

        # Experiments main frame
        self.experiments_frame = ExperimentsFrame(master=self)
        main_frame_grid_config(self.experiments_frame)

        self.new_experiment_frame = NewExperimentFrame(master=self)
        main_frame_grid_config(self.new_experiment_frame)

        # Home main frame
        self.home_frame = NewExperimentFrame(master=self)
        main_frame_grid_config(self.home_frame)

        # Default home frame
        self.home_frame.tkraise()

    def change_current_experiment_name(self, experiment_name: str):
        self.title(f"{self.app_name} - [ {experiment_name} ]")
