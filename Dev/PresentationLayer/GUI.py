import os
import shutil
import time
from datetime import datetime
from pathlib import Path
from tkinter import filedialog

import customtkinter
import open3d as o3d
from CTkMessagebox import CTkMessagebox
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

from Dev.DTOs import ImageDTO, ExperimentDTO
from Dev.LogicLayer.Service.IService import IService
from Dev.PresentationLayer.tooltip import ToolTip

absolute_path = os.path.dirname(__file__)
assets_path = os.path.join(absolute_path, "Assets")


# Wrapper class for CustomTkinter and TkinterDnD
class Tk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


# Builds drag and drop / browse files widget
def build_drag_n_drop(frame, handle_choose_file, handle_choose_directory, choose_file_title, file_types,
                      choose_directory_title, invoke_reset_wrapper=None, width=240, height=80):
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

                # Uniform main frame grid config
                def main_frame_grid_config(frame):
                    frame.grid(
                        row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                    )

                # Template import frame
                self.template_import_frame = self.TemplateImportFrame(parent_tab=self)
                main_frame_grid_config(self.template_import_frame)

                # Image export frame
                self.image_export_frame = self.ImageExportFrame(parent_tab=self)
                main_frame_grid_config(self.image_export_frame)

                # Printing object export frame
                self.printing_object_export_frame = self.PrintingObjectExportFrame(
                    parent_tab=self
                )
                main_frame_grid_config(self.printing_object_export_frame)

                # Default frame
                self.template_import_frame.tkraise()

            class ImageExportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 4), weight=1)

                    self.export_button = customtkinter.CTkButton(self, text="Export")
                    self.export_button.grid(row=1, column=1, padx=(20, 20), pady=5)

                    self.export_button = customtkinter.CTkButton(
                        self,
                        text="Convert to 3D Object",
                        command=self.handle_convert_to_printing_object_button,
                    )
                    self.export_button.grid(row=2, column=1, padx=(20, 20), pady=5)

                    self.back_button = customtkinter.CTkButton(
                        self, text="Back", command=self.handle_back_button
                    )
                    self.back_button.grid(row=3, column=1, padx=(20, 20), pady=5)

                def handle_convert_to_printing_object_button(self):
                    self.parent_tab.printing_object_export_frame.tkraise()

                def handle_back_button(self):
                    self.parent_tab.template_import_frame.tkraise()

            class PrintingObjectExportFrame(customtkinter.CTkFrame):
                def __init__(self, parent_tab):
                    super().__init__(
                        master=parent_tab.frame,
                        bg_color="transparent",
                        fg_color="transparent",
                    )
                    self.parent_tab = parent_tab
                    self.grid_columnconfigure((0, 2), weight=1)
                    self.grid_rowconfigure((0, 3), weight=1)

                    self.export_button = customtkinter.CTkButton(self, text="Export")
                    self.export_button.grid(row=1, column=1, padx=(20, 20), pady=5)

                    self.back_button = customtkinter.CTkButton(
                        self, text="Back", command=self.handle_back_button
                    )
                    self.back_button.grid(row=2, column=1, padx=(20, 20), pady=5)

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
                    print(f"works = {path}")

                def handle_choose_directory(self, path):
                    self.convert_to_image_button.configure(state=customtkinter.NORMAL)
                    print(f"works = {path}")

                def handle_convert_to_image_button(self):
                    self.parent_tab.image_export_frame.tkraise()

        class ImageTab:
            def __init__(self, master):
                self.frame = master.add("Image")
                self.frame.grid_columnconfigure(0, weight=1)
                self.frame.grid_rowconfigure(0, weight=1)

                # Uniform main frame grid config
                def main_frame_grid_config(frame):
                    frame.grid(
                        row=0, column=0, sticky=customtkinter.NS + customtkinter.EW
                    )

                # Image import frame
                self.image_import_frame = self.ImageImportFrame(parent_tab=self)
                main_frame_grid_config(self.image_import_frame)

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
                    print(os.path.dirname(file_path))
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
                    mesh = o3d.io.read_triangle_mesh(self.stl_path)
                    mesh = mesh.compute_vertex_normals()

                    o3d.visualization.draw_geometries([mesh], window_name="Converted STL",
                                                      width=800, height=800,
                                                      left=int((Tk().winfo_screenwidth() - 800) / 2),
                                                      top=int((Tk().winfo_screenheight() - 800) / 2))

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
                    self.template_path = None

                    # def view_image(path):
                    #     image = Image.open(path)
                    #
                    #     # default_width = 800
                    #     # default_height = 800
                    #     # max_val = max(image.width, image.height)
                    #     # scale_factor = default_width / max_val
                    #     # image = image.resize(
                    #     #     (
                    #     #         int(image.width * scale_factor),
                    #     #         int(image.height * scale_factor),
                    #     #     ),
                    #     #     Image.Resampling.LANCZOS,
                    #     # )
                    #     # # image = image.resize((300,300), Image.Resampling.LANCZOS)
                    #     # pic = ImageTk.PhotoImage(image)
                    #     # Orignial image: 800 x 600 => (800 x 0.25) x (600 x 0.25)  =  (200 x 150)
                    #     # Initial Canvas: 200 x 200
                    #
                    #     self.dnd.destroy()
                    #
                    #     # self.canvas = customtkinter.CTkCanvas(
                    #     #     self, width=image.width, height=image.height
                    #     # )
                    #     # self.image_id = self.canvas.create_image(
                    #     #     0, 0, image=pic, anchor="nw"
                    #     # )
                    #     # self.canvas.image = pic
                    #     # self.canvas.grid(row=0, column=1, padx=(20, 20), pady=5)
                    #     #
                    #     # self.reset_button.configure(state=tkinter.NORMAL)

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
                        invoke_reset_wrapper=self.handle_reset
                    )
                    self.dnd.grid(row=0, column=1, padx=(20, 20), pady=5)

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
                    image_dto = ImageDTO(0, self.image_path, time.time())
                    response = service.convert_image_to_template("experiment_name", image_dto)
                    if response.success:
                        self.parent_tab.build_template_export_frame(response.data.path)
                    else:
                        CTkMessagebox(icon="cancel", title="Image Converter Error", message=response.error)

                def handle_convert_to_printing_object_button(self):
                    image_dto = ImageDTO(0, self.image_path, time.time())
                    response = service.convert_image_to_printing_object("experiment_name", image_dto)
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
            self.match_button.configure(state=customtkinter.DISABLED)

        def handle_reset2():
            self.f2_is_selected = False
            self.dir2_is_selected = False
            self.match_button.configure(state=customtkinter.DISABLED)

        def dir_to_path_set(path):
            templates_set = []

            for t in os.listdir(path):
                t_path = os.path.join(path, t)
                templates_set.append(t_path)

            return tuple(templates_set)

        def handle_choose_file1(path):
            self.f1_is_selected = True
            if self.f2_is_selected or self.dir2_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set1 = (path,)

        def handle_choose_directory1(path):
            self.dir1_is_selected = True
            if self.f2_is_selected or self.dir2_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set1 = dir_to_path_set(path)

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
            self.path_set2 = (path,)

        def handle_choose_directory2(path):
            self.dir2_is_selected = True
            if self.f1_is_selected or self.dir1_is_selected:
                self.match_button.configure(state=customtkinter.NORMAL)
            self.path_set2 = dir_to_path_set(path)

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
        response = service.match("Yazan", self.path_set1, self.path_set2)
        if response.success:
            self.build_results_frame(response.data)
        else:
            CTkMessagebox(icon="cancel", title="Matching Error", message=response.error)

    def build_results_frame(self, results):
        self.results_frame = customtkinter.CTkFrame(self)
        self.results_frame.grid_columnconfigure((0), weight=1)
        self.results_frame.grid_rowconfigure((0, 6), weight=1)
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

        if len(self.path_set1) == 1 and len(self.path_set2) == 1:
            t1_name = Path(self.path_set1[0]).stem
            t2_name = Path(self.path_set2[0]).stem
            res_text = f"Score: {results}"
        elif len(self.path_set1) == 1 and len(self.path_set2) > 1:
            t1_name = Path(self.path_set1[0]).stem
            res_text = f"Matching [{t1_name}] with:\n\n"
            for t2 in self.path_set2:
                t2_name = Path(t2).stem
                res_text += f"{t2_name} - Score: {results[t2]}\n"
        elif len(self.path_set2) == 1 and len(self.path_set1) > 1:
            t2_name = Path(self.path_set2[0]).stem
            res_text = f"Matching [{t2_name}] with:\n\n"
            for t1 in self.path_set1:
                t1_name = Path(t1).stem
                res_text += f"{t1_name} - Score: {results[t1]}\n"
        elif len(self.path_set1) > 1 and len(self.path_set2) > 1:
            res_text = ""
            for t1 in self.path_set1:
                t1_name = Path(t1).stem
                res_text += f"\nMatching [{t1_name}] with:\n\n"
                for t2 in self.path_set2:
                    t2_name = Path(t2).stem
                    res_text += f"{t2_name} - Score: {results[t1][t2]}\n"

        results_label = customtkinter.CTkLabel(self.results_frame, text=res_text,
                                               font=customtkinter.CTkFont(size=16, weight="bold"))
        results_label.grid(row=1, column=0, padx=(20, 20), sticky=customtkinter.EW, pady=10)

        def handle_back_button():
            self.results_frame.destroy()

        back_button = customtkinter.CTkButton(self.results_frame, text="Back", command=handle_back_button)
        back_button.grid(
            row=2,
            column=0,
            padx=(20, 20),
            pady=(40, 5)
        )


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
            ef.destroy()

        # Build new frames
        for i, e in enumerate(experiment_dtos):
            row_frame = self.ExperimentRowFrame(
                self.scrollable_frame, index=i, experiment_name=e.name, experiment_date=e.date
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
        if response:
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
            en = get_searchable_string(e.name)
            if k in en:
                filtered_experiments_list.append(e)

        self.show_experiments_on_frame(filtered_experiments_list)

    class ExperimentRowFrame(customtkinter.CTkFrame):
        def __init__(self, master, index, experiment_name, experiment_date):
            super().__init__(
                master=master, corner_radius=10, border_width=2,
            )
            self.index = index
            self.columnconfigure((0), weight=1)
            self.rowconfigure(3, weight=1)

            self.experiment_name = experiment_name
            self.experiment_date = datetime.fromtimestamp(experiment_date).strftime("%d/%m/%Y    %H:%M:%S")
            self.experiment_info = customtkinter.CTkLabel(self, text=f"{experiment_name}    {experiment_date}")
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

        def destroy_tooltips(self):
            self.tp1.destroy()
            self.tp2.destroy()
            self.tp3.destroy()

        def handle_edit_experiment(self, e):
            pass

        def handle_continue_experiment(self, e):
            pass

        def handle_delete_experiment(self, event=None):
            response = service.delete_experiment(self.experiment_name)
            if response.success:

                for e in experiments_frame.experiment_dtos:
                    if self.experiment_name == e.name:
                        experiments_frame.experiment_dtos.remove(e)
                        experiments_frame.show_experiments_on_frame(experiments_frame.experiment_dtos)
                print(len(experiments_frame.experiment_dtos))
                CTkMessagebox(icon="check", title="Experiment",
                              message=f"Experiment {self.experiment_name} deleted successfully!")
            else:
                CTkMessagebox(icon="cancel", title="Experiments Error", message=response.error)

        class OperationRowFrame(customtkinter.CTkFrame):
            def __init__(self, master):
                super().__init__(
                    master=master, corner_radius=10, fg_color="transparent"
                )
                self.columnconfigure((0, 1, 2), weight=1)

                self.input_label = customtkinter.CTkLabel(
                    self, text="Input: john template"
                )
                self.input_label.grid(
                    row=0, column=0, sticky=customtkinter.EW, padx=(20, 20)
                )

                self.output_label = customtkinter.CTkLabel(self, text="Output: john 3D")
                self.output_label.grid(
                    row=0, column=1, sticky=customtkinter.EW, padx=(20, 20)
                )

                self.date_label = customtkinter.CTkLabel(
                    self, text="Date: 27/10/2023 14:30:17"
                )
                self.date_label.grid(
                    row=0, column=2, sticky=customtkinter.EW, padx=(20, 20)
                )


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
        pass

    def handle_continue_experiment_button(self, e):
        self.master.experiments_frame.tkraise()


class App(Tk):
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
        self.title(f"Fingerprint Biometrics Research Tool - [ {experiment_name} ]")
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
