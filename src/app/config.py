import os

class Data_file():
    #returns the path of the excel file
    def load_data_file_path(self) -> str:
        settings_path = self._create_settings_path()
        with open(settings_path) as f:
            lines = f.readlines()
        
        for line in lines:
            if line.startswith("EXCEL_FILE="):
                excel_path = line.split('=', 1)[1].strip()
            break
        return excel_path

    #puts together the path of the config file 
    def _create_settings_path(self) -> str:
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file))
        config_file = os.path.join(project_root, "app/config", "settings.txt")

        return config_file