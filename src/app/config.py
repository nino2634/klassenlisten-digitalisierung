import os
class Data_file():
    def load_data_file_path(self) -> str:
        #Load the settings file path
        settings_path = self._create_settings_path()
        with open(settings_path) as f:
            lines = f.readlines()
        
        #Load the Excel file path
        for line in lines:
            if line.startswith("EXCEL_FILE="):
                excel_path = line.split('=', 1)[1].strip()
            break
        return excel_path


    def _create_settings_path(self) -> str:
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file))
        config_file = os.path.join(project_root, "config", "settings.txt")

        return config_file