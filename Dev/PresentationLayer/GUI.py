import tkinter
import PIL.Image
import customtkinter
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import open3d as o3d
import os

absolute_path = os.path.dirname(__file__)
assets_path = os.path.join(absolute_path, "Assets")


# Wrapper class for CustomTkinter and TkinterDnD
class Tk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


# Builds drag and drop files widget
def build_drag_n_drop(frame, handle_choose_file, handle_choose_directory, choose_file_title, file_types,
                      choose_directory_title, width=240, height=80):
    dnd_frame = customtkinter.CTkFrame(
        master=frame,
        width=width,
        height=height,
        corner_radius=20,
        border_width=2,
    )
    dnd_frame.columnconfigure(0, weight=1)
    dnd_frame.rowconfigure((0, 4), weight=1)
    dnd_frame.drop_target_register(DND_FILES)

    def handle_drop(e):
        path = e.data
        if os.path.isdir(path):
            handle_choose_directory(path)
        elif os.path.isfile(path):
            handle_choose_file(path)

    dnd_frame.dnd_bind("<<Drop>>", handle_drop)

    dnd_label = customtkinter.CTkLabel(
        master=dnd_frame,
        text=f"Drag & drop files here...",
        corner_radius=20,
        width=width,
        font=customtkinter.CTkFont(slant='italic')
    )
    dnd_label.grid(row=1, column=0, sticky=customtkinter.EW, padx=10, pady=(20, 0))

    customtkinter.CTkLabel(
        master=dnd_frame,
        text="\nor\n",
        corner_radius=20,
        width=width,
    ).grid(row=2, column=0, sticky=customtkinter.EW, padx=10)

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
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(title=choose_file_title, filetypes=file_types)
        if file_path:
            handle_choose_file(file_path)

    def handle_choose_directory_event(e):
        from tkinter import filedialog
        file_path = filedialog.askdirectory(title=choose_directory_title)
        if file_path:
            handle_choose_directory(file_path)

    choose_file_label.bind("<Button-1>", handle_choose_file_event)
    choose_directory_label.bind("<Button-1>", handle_choose_directory_event)

    return dnd_frame


class SideMenuFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, corner_radius=0)
        self.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.convert_assets_button = customtkinter.CTkButton(
            self, text="Convert Assets", command=self.handle_convert_assets_button
        )
        self.convert_assets_button.grid(row=1, column=0, padx=20, pady=10)

        self.match_templates_button = customtkinter.CTkButton(
            self, text="Match Templates", command=self.handle_match_template_button
        )
        self.match_templates_button.grid(row=2, column=0, padx=20, pady=10)

        self.experiments_button = customtkinter.CTkButton(
            self, text="Experiments", command=self.handle_experiments_button
        )
        self.experiments_button.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(
            self, text="Theme:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 0))
        self.appearance_mode_optionemenu.set(
            self.appearance_mode_optionemenu._values[2]
        )

        self.scaling_label = customtkinter.CTkLabel(
            self, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(5, 10))
        self.scaling_optionemenu.set(self.scaling_optionemenu._values[2])

        self.experiments_button = customtkinter.CTkButton(
            self, text="Info", command=self.handle_experiments_button
        )
        self.experiments_button.grid(row=9, column=0, padx=20, pady=(10, 10))

    def handle_convert_assets_button(self):
        self.master.convert_assets_frame.tkraise()

    def handle_match_template_button(self):
        self.master.match_templates_frame.tkraise()

    def handle_experiments_button(self):
        self.master.experiments_frame.tkraise()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


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

                    def handle_drop(path):
                        image = Image.open(path)
                        image = image.resize((300, 300), Image.Resampling.LANCZOS)
                        self.pic = ImageTk.PhotoImage(image)

                        self.dnd.destroy()

                        self.canvas = customtkinter.CTkCanvas(self)
                        self.canvas.create_image(0, 0, image=self.pic, anchor="nw")
                        self.canvas.image = self.pic
                        self.canvas.grid(row=0, column=1, padx=(20, 20), pady=5)

                        self.back.configure(state=tkinter.NORMAL)

                    def handle_choose_file(path):
                        print(f"works = {path}")
                        handle_drop(path)

                    def handle_choose_directory(path):
                        print(f"works = {path}")

                    self.dnd = build_drag_n_drop(
                        self,
                        handle_choose_directory=handle_choose_directory,
                        handle_choose_file=handle_choose_file,
                        choose_file_title="Choose a template file",
                        file_types=[("Text files", "*.txt"), ("All files", "*.*")],
                        choose_directory_title="Choose a templates directory"
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

                    def handle_back_button():
                        self.canvas.destroy()
                        self.dnd = build_drag_n_drop(
                            self,
                            handle_choose_directory=handle_choose_directory,
                            handle_choose_file=handle_choose_file,
                            choose_file_title="Choose a template file",
                            file_types=[("Text files", "*.txt"), ("All files", "*.*")],
                            choose_directory_title="Choose a templates directory"
                        )
                        self.dnd.grid(row=0, column=1, padx=(20, 20), pady=5)
                        self.back.configure(state=tkinter.DISABLED)

                    self.back = customtkinter.CTkButton(
                        self, text="Back", command=handle_back_button
                    )
                    self.back.grid(row=3, column=1, padx=(20, 20), pady=5)
                    self.back.configure(state=tkinter.DISABLED)

                def handle_convert_to_image_button(self):
                    self.parent_tab.image_export_frame.tkraise()

                    mesh = o3d.io.read_triangle_mesh("output.stl")
                    mesh = mesh.compute_vertex_normals()
                    o3d.visualization.draw_geometries([mesh], window_name="STL")

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

                # Template export frame
                self.template_export_frame = self.TemplateExportFrame(parent_tab=self)
                main_frame_grid_config(self.template_export_frame)

                # Printing object export frame
                self.printing_object_export_frame = self.PrintingObjectExportFrame(parent_tab=self)
                main_frame_grid_config(self.printing_object_export_frame)

                # Default frame
                self.image_import_frame.tkraise()

            class TemplateExportFrame(customtkinter.CTkFrame):
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

                    self.back_button = customtkinter.CTkButton(self, text="Back", command=self.handle_back_button)
                    self.back_button.grid(row=2, column=1, padx=(20, 20), pady=5)

                def handle_back_button(self):
                    self.parent_tab.image_import_frame.tkraise()

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
                    self.parent_tab.image_import_frame.tkraise()

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

                    def view_image(path):
                        image = Image.open(path)

                        default_width = 800
                        default_height = 800
                        max_val = max(image.width, image.height)
                        scale_factor = default_width / max_val
                        image = image.resize(
                            (
                                int(image.width * scale_factor),
                                int(image.height * scale_factor),
                            ),
                            Image.Resampling.LANCZOS,
                        )
                        # image = image.resize((300,300), Image.Resampling.LANCZOS)
                        pic = ImageTk.PhotoImage(image)
                        # Orignial image: 800 x 600 => (800 x 0.25) x (600 x 0.25)  =  (200 x 150)
                        # Initial Canvas: 200 x 200

                        self.dnd.destroy()

                        self.canvas = customtkinter.CTkCanvas(
                            self, width=image.width, height=image.height
                        )
                        self.image_id = self.canvas.create_image(
                            0, 0, image=pic, anchor="nw"
                        )
                        self.canvas.image = pic
                        self.canvas.grid(row=0, column=1, padx=(20, 20), pady=5)

                        self.back.configure(state=tkinter.NORMAL)

                    def handle_choose_file(path):
                        print(f"works = {path}")
                        view_image(path)

                    def handle_choose_directory(path):
                        print(f"works = {path}")

                    self.dnd = build_drag_n_drop(
                        self,
                        handle_choose_directory=handle_choose_directory,
                        handle_choose_file=handle_choose_file,
                        choose_file_title="Choose a template file",
                        file_types=[("Text files", "*.txt"), ("All files", "*.*")],
                        choose_directory_title="Choose a templates directory"
                    )
                    self.dnd.grid(row=0, column=1, padx=(20, 20), pady=5)

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

                    def handle_back_button():
                        self.canvas.destroy()
                        self.dnd = build_drag_n_drop(
                            self,
                            handle_choose_directory=handle_choose_directory,
                            handle_choose_file=handle_choose_file,
                            choose_file_title="Choose a template file",
                            file_types=[("Text files", "*.txt"), ("All files", "*.*")],
                            choose_directory_title="Choose a templates directory"
                        )
                        self.dnd.grid(row=0, column=1, padx=(20, 20), pady=5)
                        self.back.configure(state=tkinter.DISABLED)

                    self.back = customtkinter.CTkButton(
                        self, text="Back", command=handle_back_button
                    )
                    self.back.grid(row=3, column=1, padx=(20, 20), pady=5)
                    self.back.configure(state=tkinter.DISABLED)

                def handle_convert_to_template_button(self):
                    self.parent_tab.template_export_frame.tkraise()

                def handle_convert_to_printing_object_button(self):
                    self.parent_tab.printing_object_export_frame.tkraise()


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

        def handle_choose_file(path):
            print(f"works = {path}")

        def handle_choose_directory(path):
            print(f"works = {path}")

        font = customtkinter.CTkFont(size=16, weight="bold")
        customtkinter.CTkLabel(self.frame, text="First Set", font=font).grid(row=2, column=1, padx=(20, 20),
                                                                             sticky=customtkinter.EW, pady=5)
        self.dnd1 = build_drag_n_drop(
            self.frame,
            handle_choose_directory=handle_choose_directory,
            handle_choose_file=handle_choose_file,
            choose_file_title="Choose a template file",
            file_types=[("Text files", "*.txt"), ("All files", "*.*")],
            choose_directory_title="Choose a templates directory"
        )
        self.dnd1.grid(row=3, column=1, padx=(20, 20), pady=5)

        customtkinter.CTkLabel(self.frame, text="Second Set", font=font).grid(row=2, column=2, padx=(20, 20),
                                                                              sticky=customtkinter.EW, pady=5)
        self.dnd2 = build_drag_n_drop(
            self.frame,
            handle_choose_directory=handle_choose_directory,
            handle_choose_file=handle_choose_file,
            choose_file_title="Choose a template file",
            file_types=[("Text files", "*.txt"), ("All files", "*.*")],
            choose_directory_title="Choose a templates directory"
        )
        self.dnd2.grid(row=3, column=2, padx=(20, 20), pady=5)

        self.match_button = customtkinter.CTkButton(self.frame, text="Button2")
        self.match_button.grid(
            row=4,
            columnspan=4,
            sticky=customtkinter.NS,
            padx=(20, 20),
            pady=(20, 20),
        )

        # customtkinter.
        # self.back.configure(state=tkinter.DISABLED)


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

        self.search_button = customtkinter.CTkButton(
            self.frame, text="Search", command=self.search
        )
        self.search_button.grid(
            row=0,
            column=1,
            sticky=customtkinter.NS + customtkinter.EW,
            padx=(20, 20),
            pady=(20, 20),
        )

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.frame, label_text="Experiments"
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

        self.experiments_frames = []
        for i in range(8):
            if i == 6:
                row_frame = self.ExperimentRowFrame(
                    self.scrollable_frame, index=i, fg_color="red"
                )
            else:
                row_frame = self.ExperimentRowFrame(self.scrollable_frame, index=i)

            row_frame.grid(
                row=i,
                column=0,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(20, 20),
                pady=(0, 20),
            )
            self.experiments_frames.append(row_frame)

    def search(self):
        ef = self.experiments_frames[6]

        for e in self.experiments_frames:
            e.destroy()

        # self.experiments_frames.remove(ef)
        # self.experiments_frames.append(ef)
        self.experiments_frames[0].index = ef.index
        ef.index = 0

        self.scrollable_frame.destroy()

        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.frame, label_text="Experiments"
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

        for e in self.experiments_frames:
            print("hi")
            # if i == 1:
            #     row_frame = self.ExperimentRowFrame(self.scrollable_frame, fg_color="red")
            # else:
            #     row_frame = self.ExperimentRowFrame(self.scrollable_frame)

            e.grid(
                row=e.index,
                column=0,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(20, 20),
                pady=(0, 20),
            )

    class ExperimentRowFrame(customtkinter.CTkFrame):
        def __init__(self, master, index, fg_color="transparent"):
            super().__init__(
                master=master, corner_radius=10, border_width=5, fg_color=fg_color
            )
            self.index = index
            self.columnconfigure((0), weight=1)
            self.rowconfigure(2, weight=1)

            self.search_entry = customtkinter.CTkEntry(
                self, placeholder_text="Operation name"
            )
            self.search_entry.grid(
                row=0,
                column=0,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(25, 20),
                pady=(20, 20),
            )

            self.search_button = customtkinter.CTkButton(
                self,
                text="Search",
                width=100,
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "icons8-search-256.png"))
                ),
            )
            self.search_button.grid(
                row=0, column=1, sticky=customtkinter.EW, padx=(20, 10), pady=(20, 20)
            )

            self.delete_button = customtkinter.CTkButton(
                self,
                text="Delete Experiment",
                command=self.destroy,
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "icons8-remove-80.png"))
                ),
            )
            self.delete_button.grid(
                row=0, column=2, sticky=customtkinter.EW, padx=(20, 10), pady=(20, 20)
            )

            self.export_button = customtkinter.CTkButton(
                self,
                text="Export",
                width=100,
                image=customtkinter.CTkImage(
                    Image.open(os.path.join(assets_path, "icons8-export-64.png"))
                ),
            )
            self.export_button.grid(
                row=0, column=3, sticky=customtkinter.EW, padx=(20, 25), pady=(20, 20)
            )

            self.scrollable_frame = customtkinter.CTkScrollableFrame(
                self, label_text="Operations"
            )
            self.scrollable_frame.grid(
                row=1,
                column=0,
                columnspan=4,
                sticky=customtkinter.NS + customtkinter.EW,
                padx=(20, 20),
                pady=(0, 20),
            )
            self.scrollable_frame.columnconfigure(0, weight=1)

            for i in range(10):
                row_frame = self.OperationRowFrame(self.scrollable_frame)
                row_frame.grid(
                    row=i,
                    column=0,
                    sticky=customtkinter.NS + customtkinter.EW,
                    padx=(20, 20),
                    pady=5,
                )

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


class App(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Configure app window
        app_width = 900
        app_height = 500
        self.minsize(width=app_width, height=app_height)
        self.title("Fingerprint Biometrics Research Tool")
        self.update_idletasks()
        frm_width = self.winfo_rootx() - self.winfo_x()
        win_width = self.winfo_width() + 2 * frm_width
        titlebar_height = self.winfo_rooty() - self.winfo_y()
        win_height = self.winfo_height() + titlebar_height + frm_width
        x = self.winfo_screenwidth() // 2 - win_width // 2
        y = self.winfo_screenheight() // 2 - win_height // 2
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

        # Default home frame
        self.convert_assets_frame.tkraise()


if __name__ == "__main__":
    App().mainloop()
